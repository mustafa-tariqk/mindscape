import models
from ai import ai_message
from datetime import datetime

# Initialize the Flask app
app = models.create_app()

# Define your routes here
@app.route('/')
def index():
    return "Hello world"


def start_chat(user_id):
    chat = models.Chats(user=user_id, flag=True)
    models.db.session.add(chat)
    models.db.session.commit()

"""
@id is the chat id
@message is the message sent by the user
"""
@app.route('/converse/<id>/<message>')
def converse(chat_id, message):
    ai_text = ai_message(chat_id, message)

    human = models.Messages(chat=chat_id, chat_type='Human', text=message, time=datetime.now())
    ai = models.Messages(chat=chat_id, chat_type='AI', text=ai_text, time=datetime.now())

    models.db.session.add(human)
    models.db.session.add(ai)
    models.db.session.commit()
    return ai_text


"""
Flags a chat for review
"""
@app.route('/flag/<chat_id>')
def flag_chat(chat_id):
    chat = models.Chats.query.get(chat_id)
    chat.flag = True
    models.db.session.commit()



def get_all_chats():
    chats = models.Chats.query.all()
    
    return chats



if __name__ == '__main__':
    app.run(debug=True)
