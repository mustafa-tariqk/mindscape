from flask import Flask, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from ai import ai_message
import models
from flask_login import login_manager

blueprint = make_google_blueprint(
    client_id="your-google-client-id",
    client_secret="your-google-client-secret",
    scope=["profile", "email"],
    storage=SQLAlchemyStorage(models.OAuth, models.db.session, user=current_user),
)

# Initialize the Flask app
app = models.create_app()
app.register_blueprint(blueprint, url_prefix="/login")

# Define the login manager
def require_user_type(*user_types):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not google.authorized:
                return jsonify({"error": "Authorization required"}), 403
            resp = google.get("/oauth2/v1/userinfo")
            if resp.ok:
                user_info = resp.json()
                if user_info["user_type"] not in user_types:
                    return jsonify({"error": "Forbidden"}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# Define your routes here
@app.route('/')
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v1/userinfo")
    assert resp.ok, resp.text
    return "You are {email} on Google".format(email=resp.json()["email"])

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login/google/authorized')
def google_authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    return jsonify({"data": me.data})

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


@app.route('/start_chat/<user_id>', methods=['POST'])
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


@app.route('/converse/<id>/<message>', methods=['POST'])
def converse(chat_id, message):
    """
    Adds a message to the database and returns the AI's response
    @id is the chat id
    @message is the message sent by the user
    @return the AI's response
    """
    human = models.Messages(chat=chat_id, chat_type='Human', text=message, time=datetime.now())
    
    ai_text = ai_message(chat_id, message)
    ai = models.Messages(chat=chat_id, chat_type='AI', text=ai_text, time=datetime.now())

    models.db.session.add(human)
    models.db.session.add(ai)
    models.db.session.commit()
    return ai_text


@app.route('/delete_user/<user_id>', methods=['POST'])
@require_user_type('Administrator')
def delete_user(user_id):
    """
    Deletes a user from the database
    @user_id is the id of the user to be deleted
    """
    user = models.Users.query.get(user_id)
    models.db.session.delete(user)
    models.db.session.commit()


@app.route('/delete_chat/<chat_id>', methods=['POST'])
@require_user_type('Administrator')
def delete_chat(chat_id):
    """
    Deletes a chat from the database
    @chat_id is the id of the chat to be deleted
    """
    chat = models.Chats.query.get(chat_id)
    models.db.session.delete(chat)
    models.db.session.commit()


@app.route('/flag/<chat_id>', methods=['POST'])
@require_user_type('Administrator', 'Researcher')
def flag_chat(chat_id):
    """
    Flags a chat for review
    @chat_id is the id of the chat to be flagged
    """
    chat = models.Chats.query.get(chat_id)
    chat.flag = True
    models.db.session.commit()


@app.route('/get_all_chats', methods=['GET'])
@require_user_type('Administrator', 'Researcher')
def get_all_chats():
    """
    @return a dictionary of all chats and their messages
    """
    chat_dict = {}
    for chat in models.Chats.query.all():
        messages = models.Messages.query.filter_by(chat=chat.id).order_by(
                                                models.Messages.time).all()
        chat_dict[chat.id] = [message.text for message in messages]
    
    return chat_dict


if __name__ == '__main__':
    app.run(debug=True)
