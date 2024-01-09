import models
from ai import ai_message
from datetime import datetime

# Initialize the Flask app
app = models.create_app()

# Define your routes here
@app.route('/')
def index():
    return "Hello world"

def human_response(id, chat, text):
    message = models.Messages(chat=id, chat_type='Human', text=text, time=datetime.now())
    models.db.session.add(message)
    models.db.session.commit()

def ai_response(id, chat):
    response = ai_message(chat)
    message = models.Messages(chat=id, chat_type='AI', text=response, time=datetime.now())
    models.db.session.add(message)
    models.db.session.commit()
    return response


if __name__ == '__main__':
    app.run(debug=True)
