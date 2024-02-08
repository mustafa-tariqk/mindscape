"""
Models to be held in the database
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import csv

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


class Languages(db.Model):  # pylint: disable=too-few-public-methods
    """
    Languages Model
    Contains supported languages and the corresponding metadata.
    """
    __tablename__ = 'languages'
    id = db.Column(db.Text, primary_key = True) # the language name
    sample_size = db.Column(db.Integer, nullable=False) # for weight calculations
    mean_count = db.Column(db.Integer, nullable=False) # for words not in database


class Words(db.Model):  # pylint: disable=too-few-public-methods
    """
    Word Weights Model
    Represents the weights of common words in the used language. Meant for retrieval by certain analytics functions
    """
    __tablename__ = 'words'
    id = db.Column(db.Text, primary_key = True) # the word itself
    language = db.Column(db.Text, db.ForeignKey('languages.id'), nullable = False)
    count = db.Column(db.Integer, nullable = False) # frequency
    db.ForeignKeyConstraint(['language'], ['languages.id'], ondelete='CASCADE') # dependency


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

        # seed language and word weight
        language = User.query.filter_by(id="english").first()
        if not language:
            language = Languages(id="english", sample_size=0, mean=0)
            db.session.add(language)
            db.session.commit()

        # multi-language support should start here
        if not User.query.filter_by(language="english").first(): # maybe problematic if you want to update words
            sample_size = 0
            word_count = 0
            with open('./data/english_freq.csv', newline='') as csvfile:
                rows = csv.reader(csvfile, delimiter=' ', quotechar='|')
                for word, count in rows:
                    sample_size += count 
                    word_count += 1
                    word = Words(id=word, language=language.id, count=count)
            
            language.sample_size = sample_size
            language.mean_count = sample_size // word_count


    return app
