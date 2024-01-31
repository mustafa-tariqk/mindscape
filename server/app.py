"""
This is the main file for the server. It contains all the routes and
the logic for the routes.
"""
import time
from datetime import datetime
from functools import wraps
from os import environ
from dotenv import load_dotenv
from flask import redirect, request, url_for
from flask_dance.contrib.google import google, make_google_blueprint
import models
from ai import ai_message

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
    return f"You are {email} on Google"


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
    return str(chat.id)


@app.route("/converse/<chat_id>/<message>")
@role_required("Administrator", "Researcher", "Contributor")
def converse(chat_id, message):
    """
    Adds a message to the database and returns the AI's response
    @id is the chat id
    @message is the message sent by the user
    @return the AI's response
    """
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
    return ai_text


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
    return "User deleted"


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
    return "User permission changed to " + role


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
    return "Chat deleted"


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
    return "Chat flagged"


@app.route("/get_all_chats")
@role_required("Administrator", "Researcher")
def get_all_chats():
    """
    @return a dictionary of all chats and their messages
    """
    chat_dict = {}
    for chat in models.Chats.query.all():
        messages = (
            models.Messages.query.filter_by(chat=chat.id)
            .order_by(models.Messages.time)
            .all()
        )
        chat_dict[chat.id] = [message.text for message in messages]
    return chat_dict


if __name__ == "__main__":
    app.run(debug=True)
