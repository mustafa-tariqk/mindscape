from datetime import datetime
import models
from ai import ai_message

# Initialize the Flask app
app = models.create_app()

# Define your routes here
@app.route('/')
def index():
    return "Server is running!"


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
def delete_user(user_id):
    """
    Deletes a user from the database
    @user_id is the id of the user to be deleted
    """
    user = models.Users.query.get(user_id)
    models.db.session.delete(user)
    models.db.session.commit()

@app.route('/delete_chat/<chat_id>', methods=['POST'])
def delete_chat(chat_id):
    """
    Deletes a chat from the database
    @chat_id is the id of the chat to be deleted
    """
    chat = models.Chats.query.get(chat_id)
    models.db.session.delete(chat)
    models.db.session.commit()


@app.route('/flag/<chat_id>', methods=['POST'])
def flag_chat(chat_id):
    """
    Flags a chat for review
    @chat_id is the id of the chat to be flagged
    """
    chat = models.Chats.query.get(chat_id)
    chat.flag = True
    models.db.session.commit()


@app.route('/get_all_chats', methods=['GET'])
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
