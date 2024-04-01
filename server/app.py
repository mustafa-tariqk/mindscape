"""
This is the main file for the server. It contains all the routes and
the logic for the routes.
"""
import time
from datetime import datetime
from functools import wraps
from os import environ
from dotenv import load_dotenv
from flask import redirect, request, url_for, jsonify, session
from flask_dance.contrib.google import google, make_google_blueprint
from flask_cors import CORS, cross_origin

import models
import controllers.analytics as analytics
import controllers.utils.database as database
import controllers.utils.vstore as vstore
from controllers.utils.ai import ai_message, llm_embedder, categorize_submission, summarize_submission

import faiss

load_dotenv()

blueprint = make_google_blueprint(
    client_id=environ.get("GOOGLE_CLIENT_ID"),
    client_secret=environ.get("GOOGLE_CLIENT_SECRET"),
    scope=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
    ],
    redirect_url="/login",
)

app = models.create_app()
app.secret_key = environ.get("FLASK_SECRET_KEY")
app.register_blueprint(blueprint, url_prefix="/login")
CORS(app, resources={r"*": {"origins": "*"}}, supports_credentials=True)
app.config["TESTING"] = bool(int(environ.get("TESTING", 1)))

SIMILARITY_THRESHOLD = 0.8 # threshold of similarity that, if surpassed, will result in a new cluster with this chat as centre

def cluster_all_chats(k=5):
    """
    Clusters all chats into experiences. Using k-means clustering.
    Will rewrite the entire experience table as well as reassign the experience field in the chat table.
    @param k: The number of clusters to create
    """
    models.Experiences.query.delete() # clear the table
    models.db.session.commit() # experience field in chat table will be set to null

    chats = models.Chats.query.filter_by(flag=False).all() # get all the chats, potentially not a good idea, consider just using id
    if len(chats) == 0:
        return # no chats to cluster
    chats_vstore = vstore.create_chats_vectorstore(chats, llm_embedder)

    embeddings = [llm_embedder.embed_query(chat.summary) for chat in chats] # RAM intensive, also may waste tokens

    # cluster using faiss.KMeans
    kmeans = faiss.Kmeans(len(embeddings[0]), k, niter=20, verbose=True)
    kmeans.train(embeddings)

    # assign the closest chat to the centroid as the centroid
    for i in range(k):
        closest_chat_doc, _ = vstore.get_k_nearest_by_vector(kmeans.centroids[i], chats_vstore, 1)[0]
        # assign closest chat as a experience, maybe give it a name
        closest_chat = models.Chats.query.get(closest_chat_doc.page_content)
        models.db.session.add(models.Experiences(name=closest_chat.summary, id=closest_chat.id))
        models.db.session.commit()

    # assign the chat to the closest experience
    experiences = models.Experiences.query.all()
    exp_vstore = vstore.create_exp_vectorstore(experiences, llm_embedder)
    for chat in chats:
        closest_exp_docs, _ = vstore.get_k_nearest_by_vector(llm_embedder.embed_query(chat.summary), exp_vstore, 1)[0]
        closest_exp = models.Experiences.query.get(closest_exp_docs.page_content)
        chat.experience = closest_exp.id
        closest_exp.count += 1
        models.db.session.commit()

# print("Clustering all chats")
# with app.app_context():
#     cluster_all_chats(7) # Cluster on first start

# print("Clustering complete")

# decorator to check user type
def role_required(*roles):
    """
    This decorator checks if the user is authorized with Google. If not, it
    redirects to the Google login page. Then it retrieves the user's email from
    the Google API and checks if the user has the required role.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not app.config["TESTING"]:
                if not google.authorized or google.token["expires_at"] <= time.time():
                    return {"error": "Unauthorized"}, 401
                email = session["google_auth"]["email"]
                user = models.User.query.filter_by(email=email).first()
                if user is None:
                    user = models.User(email=email, user_type="Contributor")
                    models.db.session.add(user)
                    models.db.session.commit()
                if user.user_type not in roles:
                    return {"error": "User does not have the required role"}, 403
            return f(*args, **kwargs)

        return decorated_function

    return decorator


@cross_origin()
@app.route("/login")
def login():
    """
    Redirects to the Google login page, then back to the homepage
    """
    if not google.authorized or google.token["expires_at"] <= time.time():
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    session['google_auth'] = resp.json()
    return redirect(environ.get("CLIENT_URL"))


@cross_origin()
@app.route("/logout")
def logout():
    """
    Logs the user out and redirects to the homepage
    """
    session.clear()
    return redirect(environ.get("CLIENT_URL"))


@cross_origin()
@app.route("/api/user")
@role_required("Administrator", "Researcher", "Contributor")
def index():
    """
    This function returns the user's email, user_id, and role.
    """
    if app.config["TESTING"]:
        email = "neuma.mindscape@gmail.com"
    else:
        email = session["google_auth"]["email"]
    user = models.User.query.filter_by(email=email).first()
    return {"email": user.email, "user_id": user.id, "role": user.user_type}


@cross_origin()
@app.route("/api/start_chat/<user_id>")
@role_required("Administrator", "Researcher", "Contributor")
def start_chat(user_id):
    """
    Creats a new chat in the database
    @user_id is the id of the user starting the chat
    @return the id of the new chat
    """
    chat = models.Chats(user=user_id)
    models.db.session.add(chat)
    models.db.session.commit()
    return {"chat_id": chat.id}


@cross_origin()
@app.route("/api/converse", methods=["POST"])
@role_required("Administrator", "Researcher", "Contributor")
def converse():
    """
    Adds a message to the database and returns the AI's response
    @request: {chat_id: int, message: str}
    @return the AI's response
    """
    request_body = request.get_json()
    chat_id = request_body['chat_id']
    message = request_body['message']
    human = models.Messages(
        chat=chat_id, chat_type="Human", text=message, time=datetime.now()
    )

    ai_text = ai_message(chat_id, message)
    ai = models.Messages(
        chat=chat_id, chat_type="AI", text=ai_text, time=datetime.now()
    )

    models.db.session.add(human)
    models.db.session.add(ai)
    models.db.session.commit()

    return {"ai_response": ai_text}


@cross_origin()
@app.route("/api/get_trolls")
@role_required("Administrator")
def get_trolls():
    """
    @return {email: str, flag_count: int}
    """
    trolls = {}
    for chat in models.Chats.query.all():
        user = models.User.query.filter_by(id=chat.user).first()
        if chat.flag:
            if user.email not in trolls:
                trolls[user.email] = 0
            trolls[user.email] += 1
    return dict(sorted(trolls.items(), key=lambda item: item[1]))


@cross_origin()
@app.route("/api/delete_user/<user_email>")
@role_required("Administrator")
def delete_user(user_email):
    """
    Deletes a user from the database
    @user_email is the email of the user to be deleted
    """
    user = models.User.query.filter_by(email=user_email).first()
    if user is None:
        return {"error": "User not found"}, 404
    models.db.session.delete(user)
    models.db.session.commit()
    return {"user_email": user.email, "status": "deleted" }


@cross_origin()
@app.route("/api/change_permission/<user_email>/<role>")
@role_required("Administrator")
def change_permission(user_email, role):
    """
    Changes the permission of a user
    @user_email is the email of the user to be changed
    @role is the new role of the user
    """
    if role not in ["Administrator", "Researcher", "Contributor"]:
        raise ValueError("Invalid role")
    user = models.User.query.filter_by(email=user_email).first()
    if user is None:
        return {"error": "User not found"}, 404
    user.user_type = role
    models.db.session.commit()
    return {"user_email": user.email, "role": user.user_type}


@cross_origin()
@app.route("/api/delete_chat/<chat_id>")
@role_required("Administrator")
def delete_chat(chat_id):
    """
    Deletes a chat from the database
    @chat_id is the id of the chat to be deleted
    """
    chat = models.Chats.query.filter_by(id=chat_id).first()
    models.db.session.delete(chat)
    models.db.session.commit()
    return {"chat_id": chat.id, "status": "deleted"}


@cross_origin()
@app.route("/api/flag/<chat_id>")
@role_required("Administrator", "Researcher")
def flag_chat(chat_id):
    """
    Flags a chat for review
    @chat_id is the id of the chat to be flagged
    """
    chat = models.Chats.query.filter_by(id=chat_id).first()
    chat.flag = True
    models.db.session.commit()
    return {"chat_id": chat.id, "status": "flagged"}


@cross_origin()
@app.route("/api/get_all_chats")
@role_required("Administrator", "Researcher")
def get_all_chats():
    """
    @return a dictionary of all chats and their messages
    """
    chat_dict = {}
    for chat in models.Chats.query.all():
        messages = database.get_all_chat_messages(chat.id)
        chat_dict[chat.id] = [message.text for message in messages]
    return chat_dict


@cross_origin()
@app.route("/api/submit", methods=["POST"])
@role_required("Administrator", "Researcher", "Contributor")
def submit():
    """
    Handles submission of the chat
    @request: {chat_id: int, test: bool}
    @return schema: {
        "submitter_info": {"Weight": string, "Height": string, "Age": int},
        "substance_info": list [{"Dose": string, "Method": string, "Substance": string}]
    }
    schema could change on request, but it's an object fs
    """
    request_body = request.get_json()
    chat_id = int(request_body['chatId'])
    if "test" in request_body:
        test = request_body['test']

        if test: # could it be null
            return jsonify({
                "submitter_info": {"Weight": "200 lbs", "Height": "200 cm", "Age": 25},
                "substance_info": [{"Dose": "200 mg", "Method": "Oral", "Substance": "Caffeine"}]
            })
    
    result = {}
    with app.app_context():
        result = categorize_submission(chat_id)
        database.new_chat_category(chat_id, result)

        # write to database
        summary = summarize_submission(chat_id)
        database.update_chat_summary(chat_id, summary)
        database.update_chat_flag(chat_id, False) # unflag only on submission, could add additional logic

        exp_vstore = vstore.create_exp_vectorstore(models.Experiences.query.all(), llm_embedder)
        closest_exp_doc, similarity_score = vstore.cluster_new_chat(database.get_chat(chat_id), exp_vstore)
        if similarity_score <= SIMILARITY_THRESHOLD:
            exp_id = int(closest_exp_doc.page_content) # remember, page content is always the id
            database.update_chat_exp(chat_id, exp_id) 

        else: # create new experience
            new_exp = models.Experiences(name=summary, id=chat_id)
            models.db.session.add(new_exp)
            models.db.session.commit()
            database.update_chat_exp(chat_id, chat_id)

    return jsonify(result)


@cross_origin()
@app.route("/api/analytics/get_frequent_words", methods=["GET"])
@role_required("Administrator", "Researcher", "Contributor")
def get_frequent_words():
    """
    @return schema {
        'global_count': frequency in language distribution,
        'local_count': frequency in chat,
        'global_max - global_count': difference from the most used word,
        'weight': attributed weight
    }
    """
    chat_id = request.args.get("chat_id", type=int)
    k = request.args.get("k", type=int)
    test = request.args.get("test", default=False, type=bool)
    if test:
        chat_id = None
    with app.app_context():
        return jsonify(analytics.get_k_weighted_frequency(chat_id, k))
    

@cross_origin()
@app.route("/api/analytics/experience", methods=["GET"])
@role_required("Administrator", "Researcher", "Contributor")
def experience():
    """
    @return schema {
        "experiences": [{
            "name": "",
            "similarity": 0.0 // float 
            "percentage": 0 // int in range [0, 100], percentage of submission with this experience
        }]
    }
    """
    test = request.args.get("test", default=False, type=bool)
    if test:
        return jsonify({
            "experiences": [{
                "name": "Infinite Power",
                "similarity": 0.3,
                "percentage": 20.0
            }, {
                "name": "Signature Look of Authority",
                "similarity": 0.1,
                "percentage": 30.0
            }, {
                "name": "I am your father",
                "similarity": 0.05,
                "percentage": 50.0
            }]
        })
    
    else:
        chat_id = request.args.get("chat_id", type=int)
        k = request.args.get("k", type=int)
        return jsonify(analytics.get_experience_data(chat_id, k))
    
@cross_origin()
@app.route("/api/analytics/cluster_chats", methods=["POST"])
@role_required("Administrator")
def cluster_chats():
    """
    Clusters all chats into experiences. Using k-means clustering.
    Will rewrite the entire experience table as well as reassign the experience field in the chat table.
    @return the id of the new chat
    """
    request_body = request.get_json()
    k = request_body['k']
    cluster_all_chats(k)
    return {"status": "success"}


if __name__ == "__main__":
    app.run(port=8080, debug=True)
