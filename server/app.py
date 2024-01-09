import models
from ai import ai_message
from datetime import datetime

# Initialize the Flask app
app = models.create_app()

# Define your routes here
@app.route('/')
def index():
    return "Hello world"


"""
@id is the chat id
@message is the message sent by the user
"""
@app.route('/converse/<id>/<message>')
def converse(id, message):
    ai_text = ai_message(id, message)

    human = models.Messages(chat=id, chat_type='Human', text=message, time=datetime.now())
    ai = models.Messages(chat=id, chat_type='AI', text=ai_text, time=datetime.now())

    models.db.session.add(human)
    models.db.session.add(ai)
    models.db.session.commit()
    return ai_text



if __name__ == '__main__':
    app.run(debug=True)
