"""
This is the main file for the server. It contains all the routes and
the logic for the routes.
"""
import time
from datetime import datetime
from functools import wraps
from os import environ
from dotenv import load_dotenv
from flask import redirect, request, url_for, jsonify
from flask_dance.contrib.google import google, make_google_blueprint
from flask_cors import CORS

import models
import utils
from analytics.wordcloud import get_k_weighted_frequency
from analytics.vstore_handler import create_vectorstores, cluster_new_message, new_experience
from ai import ai_message, llm_embedder

load_dotenv()

blueprint = make_google_blueprint(
    client_id=environ.get("GOOGLE_CLIENT_ID"),
    client_secret=environ.get("GOOGLE_CLIENT_SECRET"),
    scope=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
    ],
)

# Initialize the Flask app
app = models.create_app()
app.secret_key = environ.get("FLASK_SECRET_KEY")
app.register_blueprint(blueprint, url_prefix="/login")

# uncomment line below to skip auth
# app.config["TESTING"] = True
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
                    return redirect(url_for("google.login", next=request.url))
                resp = google.get("/oauth2/v2/userinfo")
                assert resp.ok, resp.text
                email = resp.json()["email"]
                user = models.User.query.filter_by(email=email).first()
                if user is None or user.user_type not in roles:
                    return "You do not have permission to perform this action."
            return f(*args, **kwargs)

        return decorated_function

    return decorator


# Define your routes here
@app.route("/")
def index():
    """
    This function checks if the user is authorized with Google. If not, it
    redirects to the Google login page. Then it retrieves the user's email from
    the Google API and returns a message with the email address.
    """
    if not app.config["TESTING"]:
        if not google.authorized or google.token["expires_at"] <= time.time():
            return redirect(url_for("google.login"))
        resp = google.get("/oauth2/v2/userinfo")
        assert resp.ok, resp.text
        email = resp.json()["email"]
        user = models.User.query.filter_by(email=email).first()
        if user is None:
            user = models.User(email=email, user_type="Contributor")
            models.db.session.add(user)
            models.db.session.commit()
        # redirect this to front end when it's ready.
        return {"email": email, "user_id": user.id}
    else:
        user = models.User.query.filter_by(email="neuma.mindscape@gmail.com").first()
        return {"email": user.email, "user_id": user.id}


@app.route("/start_chat/<user_id>")
# @role_required("Administrator", "Researcher", "Contributor")
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


@app.route("/converse/", methods=["POST"])
# @role_required("Administrator", "Researcher", "Contributor")
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


@app.route("/delete_user/<user_id>")
# @role_required("Administrator")
def delete_user(user_id):
    """
    Deletes a user from the database
    @user_id is the id of the user to be deleted
    """
    user = models.User.query.get(user_id)
    models.db.session.delete(user)
    models.db.session.commit()
    return {"user_id": user.id, "status": "deleted" }


@app.route("/change_permission/<user_id>/<role>")
# @role_required("Administrator")
def change_permission(user_id, role):
    """
    Changes the permission of a user
    @user_id is the id of the user to be changed
    @role is the new role of the user
    """
    if role not in ["Administrator", "Researcher", "Contributor"]:
        raise ValueError("Invalid role")
    user = models.User.query.get(user_id)
    user.user_type = role
    models.db.session.commit()
    return {"user_id": user.id, "role": user.user_type}


@app.route("/delete_chat/<chat_id>")
# @role_required("Administrator")
def delete_chat(chat_id):
    """
    Deletes a chat from the database
    @chat_id is the id of the chat to be deleted
    """
    chat = models.Chats.query.get(chat_id)
    models.db.session.delete(chat)
    models.db.session.commit()
    return {"chat_id": chat.id, "status": "deleted"}


@app.route("/flag/<chat_id>")
# @role_required("Administrator", "Researcher")
def flag_chat(chat_id):
    """
    Flags a chat for review
    @chat_id is the id of the chat to be flagged
    """
    chat = models.Chats.query.get(chat_id)
    chat.flag = True
    models.db.session.commit()
    return {"chat_id": chat.id, "status": "flagged"}


@app.route("/get_all_chats")
# @role_required("Administrator", "Researcher")
def get_all_chats():
    """
    @return a dictionary of all chats and their messages
    """
    chat_dict = {}
    for chat in models.Chats.query.all():
        messages = utils.get_all_chat_messages(chat.id)
        chat_dict[chat.id] = [message.text for message in messages]
    return chat_dict


@app.route("/analytics/get_frequent_words/", methods=["GET"])
# @role_required("Contributor")
def get_frequent_words():
    """
    @return a dictionary of the most frequent words in the chat
    """
    chat_id = request.args.get("chat_id")
    k = int(request.args.get("k"))
    return jsonify(get_k_weighted_frequency(k, chat_id))


if __name__ == "__main__":
    app.run(debug=True)#, ssl_context=('cert.pem', 'key.pem')
