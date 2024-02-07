"""
Models to be held in the database
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Database object


class User(db.Model):  # pylint: disable=too-few-public-methods
    """
    User Model
    Represents a user in the database. Users are either Administrators, 
    Researchers, or Contributors.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    user_type = db.Column(
        db.Enum('Administrator', 'Researcher', 'Contributor'), nullable=False)


class Chats(db.Model):  # pylint: disable=too-few-public-methods
    """
    Chat Model
    Represents a chat in the database. Each chat is associated with a user.
    """
    __tablename__ = 'chats'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    flag = db.Column(db.Boolean, nullable=False)
    db.ForeignKeyConstraint(['user'], ['users.id'], ondelete='CASCADE')


class Messages(db.Model):  # pylint: disable=too-few-public-methods
    """
    Messages Model
    Represents a message in the database. Each message is associated with a chat.
    """
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    chat = db.Column(db.Integer, db.ForeignKey('chats.id'), nullable=False)
    chat_type = db.Column(db.Enum('Human', 'AI'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    db.ForeignKeyConstraint(['chat'], ['chats.id'], ondelete='CASCADE')


class WordWeights(db.Model):  # pylint: disable=too-few-public-methods
    """
    Word Weights Model
    Represents the weights of common words in the used language. Meant for retrieval by certain analytics functions
    """
    __tablename__ = 'word_weights'
    id = db.Column(db.Text, primary_key = True)
    count = db.Column(db.Integer, nullable = False)


def create_app():
    """
    Initializes the Flask app and database
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    db.init_app(app)

    with app.app_context():
        db.create_all()  # Create database and tables if they don't exist
        # make an admin user
        if not User.query.filter_by(email="neuma.mindscape@gmail.com").first():
            admin = User(email="neuma.mindscape@gmail.com",
                         user_type="Administrator")
            db.session.add(admin)
            db.session.commit()

    return app
