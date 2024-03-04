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
from ai import ai_message, handle_submission

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
CORS(app, resources={r"*": {"origins": "*"}}, supports_credentials=True)
app.config["TESTING"] = bool(int(environ.get("TESTING", 0)))



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
                if user is None or user.user_type not in roles:
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
@app.route("/")
@role_required("Administrator", "Researcher", "Contributor")
def index():
    """
    This function returns the user's email and user_id
    """
    if app.config["TESTING"]:
        user = models.User.query.filter_by(email="neuma.mindscape@gmail.com").first()
        return {"email": user.email, "user_id": user.id}
    email = session["google_auth"]["email"]
    user = models.User.query.filter_by(email=email).first()
    if user is None:
        user = models.User(email=email, user_type="Contributor")
        models.db.session.add(user)
        models.db.session.commit()
    return {"email": email, "user_id": user.id}


@cross_origin()
@app.route("/start_chat/<user_id>")
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
@app.route("/converse/", methods=["POST"])
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
@app.route("/submit/", methods=["POST"])
@role_required("Administrator", "Researcher", "Contributor")
def submit():
    """
    Handles submission of the chat
    @request: {chat_id: int}
    @return schema: {weight: int, height: int, substance: string}
    schema could change on request, but it's an object fs
    """
    request_body = request.get_json()
    chatId = request_body['chatId']
    result = {}
    with app.app_context():
        result = handle_submission(chatId)
    return result


@cross_origin()
@app.route("/delete_user/<user_id>")
@role_required("Administrator")
def delete_user(user_id):
    """
    Deletes a user from the database
    @user_id is the id of the user to be deleted
    """
    user = models.User.query.get(user_id)
    models.db.session.delete(user)
    models.db.session.commit()
    return {"user_id": user.id, "status": "deleted" }


@cross_origin()
@app.route("/change_permission/<user_id>/<role>")
@role_required("Administrator")
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


@cross_origin()
@app.route("/delete_chat/<chat_id>")
@role_required("Administrator")
def delete_chat(chat_id):
    """
    Deletes a chat from the database
    @chat_id is the id of the chat to be deleted
    """
    chat = models.Chats.query.get(chat_id)
    models.db.session.delete(chat)
    models.db.session.commit()
    return {"chat_id": chat.id, "status": "deleted"}


@cross_origin()
@app.route("/flag/<chat_id>")
@role_required("Administrator", "Researcher")
def flag_chat(chat_id):
    """
    Flags a chat for review
    @chat_id is the id of the chat to be flagged
    """
    chat = models.Chats.query.get(chat_id)
    chat.flag = True
    models.db.session.commit()
    return {"chat_id": chat.id, "status": "flagged"}


@cross_origin()
@app.route("/get_all_chats")
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


@app.route("/analytics/get_frequent_words/", methods=["GET"])
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
    k = int(request.args.get("k"))
    with app.app_context():
        return jsonify(get_k_weighted_frequency(k, chat_id))


if __name__ == "__main__":
    app.run(port=8080, debug=True)
