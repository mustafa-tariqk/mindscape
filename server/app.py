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
import utils
from analytics.wordcloud import get_k_weighted_frequency
from analytics.vstore_handler import create_vectorstores, cluster_new_message, new_experience
from ai import ai_message, llm_embedder, handle_submission

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

# Initialize the Flask app
app = models.create_app()
app.secret_key = environ.get("FLASK_SECRET_KEY")
app.register_blueprint(blueprint, url_prefix="/login")

# uncomment line below to skip auth
app.config["TESTING"] = True
CORS(app)

# Initialize vectorstores
with app.app_context():
    message_vstore, exp_vstore = create_vectorstores(utils.get_all_chat_messages(), llm_embedder, utils.get_all_experiences())


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
                    return {"error": "Unauthorized"}
                email = session["google_auth"]["email"]
                user = models.User.query.filter_by(email=email).first()
                if user is None:
                    user = models.User(email=email, user_type="Contributor")
                    models.db.session.add(user)
                    models.db.session.commit()
                if user.user_type not in roles:
                    return {"error": "User does not have the required role"}
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
    This function returns the user's email and user_id
    """
    if app.config["TESTING"]:
        email = "neuma.mindscape@gmail.com"
    else:
        email = session["google_auth"]["email"]
    user = models.User.query.filter_by(email=email).first()
    return {"email": user.email, "user_id": user.id}


@cross_origin()
@app.route("/api/start_chat/<user_id>")
@role_required("Administrator", "Researcher", "Contributor")
def start_chat(user_id):
    """
    Creats a new chat in the database
    @user_id is the id of the user starting the chat
    @return the id of the new chat
    """
    chat = models.Chats(user=user_id, flag=False)
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

    # vectorstore shenanigans
    message, new = cluster_new_message(human, message_vstore, exp_vstore, 100) # Arbitrary threshold for now
    if new: # new cluster
        exp = models.Experiences() # TODO: prompt the model to name the experience
    else: # increment cluster count
        exp = models.Experiences.query.get(message.experience)
        exp.count += 1

    models.db.session.commit()

    return {"ai_response": ai_text}


@cross_origin()
@app.route("/api/submit", methods=["POST"])
@role_required("Administrator", "Researcher", "Contributor")
def submit():
    """
    Handles submission of the chat
    @request: {chat_id: int, test: bool}
    @return schema: {weight: int, height: int, substance: string}
    schema could change on request, but it's an object fs
    """
    request_body = request.get_json()
    chatId = request_body['chatId']
    test = request_body['test']
    if test: # could it be null
        return jsonify({"weight in kg":75, "height in cm":178, "substance":"Lean"})
    result = {}
    with app.app_context():
        result = handle_submission(chatId)
    return jsonify(result)


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
        messages = utils.get_all_chat_messages(chat.id)
        chat_dict[chat.id] = [message.text for message in messages]
    return chat_dict


@cross_origin()
@app.route("/api/analytics/get_frequent_words", methods=["GET"])
@role_required("Contributor")
def get_frequent_words():
    """
    @return schema {
        'global_count': frequency in language distribution,
        'local_count': frequency in chat,
        'global_max - global_count': difference from the most used word,
        'weight': attributed weight
    }
    """
    chat_id = request.args.get("chat_id")
    k = request.args.get("k", type=int)
    test = request.args.get("test", default=False, type=bool)
    if test:
        chat_id = None
    with app.app_context():
        return jsonify(get_k_weighted_frequency(k, chat_id))
    

@cross_origin()
@app.route("/api/analytics/experience", methods=["GET"])
@role_required("Contributor")
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
                "similarity": 300.0,
                "percentage": 20
            }, {
                "name": "Signature Look of Authority",
                "similarity": 100.0,
                "percentage": 30
            }, {
                "name": "I am your father",
                "similarity": 50.0,
                "percentage": 50
            }]
        })


if __name__ == "__main__":
    app.run(port=8080, debug=True)
