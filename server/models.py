"""
Models to be held in the database
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import csv
import nltk
import json
import os

from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import FAISS as faiss # I don't like capitals

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
    language = db.Column(db.Text, db.ForeignKey('languages.id'), nullable=False, default='english')
    experience = db.Column(db.Integer, db.ForeignKey('experiences.id'), nullable=True, default=None) # flagged submissions will have null here
    summary = db.Column(db.Text, nullable=True) # this will be used to embed the chat

    db.ForeignKeyConstraint(['user'], ['users.id'], ondelete='CASCADE')
    # should the chats be deleted if languages are not supported?
    db.ForeignKeyConstraint(['language'], ['languages.id'], ondelete='CASCADE')
    db.ForeignKeyConstraint(['experience'], ['experiences.id'], ondelete='NULL')


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
    # embedding = db.Column(db.Text, nullable=True, default=None) # contains the id of the corresponding doc in vectorstore
    # experience = db.Column(db.Integer, db.ForeignKey('experiences.id'), nullable=True) # flagged submissions will have null here
    # centroid = db.Column(db.Boolean, nullable = False, default=False) # if this message is a centroid replacement
    db.ForeignKeyConstraint(['chat'], ['chats.id'], ondelete='CASCADE')
    # db.ForeignKeyConstraint(['experience'], ['experiences.id'], ondelete='NULL') # primed for reclustering


class Languages(db.Model):  # pylint: disable=too-few-public-methods
    """
    Languages Model
    Contains supported languages and the corresponding metadata.
    """
    __tablename__ = 'languages'
    # the language name, use print(nltk.corpusstopwords.fileids()) to see what's available
    id = db.Column(db.Text, primary_key = True) 
    sample_size = db.Column(db.Integer, nullable=False, default=0) # for weight calculations
    mean_count = db.Column(db.Integer, nullable=False, default=0) 
    max_count = db.Column(db.Integer, nullable=False, default=0) # detect common words
    min_count = db.Column(db.Integer, nullable=False, default=0) # for words that are not in the distribution
    # standard_deviation = db.Column(db.Float, nullable=False, default=0) # for weight calculations


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


class Experiences(db.Model): # pylint: disable=too-few-public-methods
    """
    Experience Tag Model
    Represents the different experience clusters.
    """
    __tablename__ = 'experiences'
    id = db.Column(db.Integer, db.ForeignKey('chats.id'), nullable = False, primary_key = True) # the chat that is set as the centroid
    name = db.Column(db.Text, nullable = False) # name of the experience in English (default language)
    count = db.Column(db.Integer, nullable = False, default = 1) # how many in cluster
    db.ForeignKeyConstraint(['centroid'], ['chats.id'], ondelete='CASCADE') # must be replaced if the centroid is deleted

class Chats_Categories(db.Model): # pylint: disable=too-few-public-methods
    """
    Models the relationship between the different chats and some categorizations.
    In this case, Chat-Substance pair will be the default key pair.
    Because of this, some chats may appear multiple times if multiple substances were used.
    Weight is assumed to be in kg.
    """
    __tablename__ = 'chats_categories'
    chat = db.Column(db.Integer, db.ForeignKey('chats.id'), nullable=False, primary_key=True)
    dose = db.Column(db.Text, nullable=False, primary_key=True)
    method = db.Column(db.Text, nullable=False, primary_key=True)
    substance = db.Column(db.Text, nullable=False, primary_key=True)
    age = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Integer, nullable=True)
    db.ForeignKeyConstraint(['chat'], ['chats.id'], ondelete='CASCADE')


def create_app():
    """
    Initializes the Flask app and database
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    db.init_app(app)

    nltk.download("stopwords") # Stopwords library
    nltk.download("punkt") # Tokenizer
    # print(nltk.corpus.stopwords.fileids()) # To show the available languages

    with app.app_context():
        db.create_all()  # Create database and tables if they don't exist
        # seed language
        language = Languages.query.filter_by(id="english").first()
        if not language:
            language = Languages(id="english", sample_size=0, mean_count=0)
            db.session.add(language)
            db.session.commit()

        # make an admin user
        if not User.query.filter_by(email="neuma.mindscape@gmail.com").first():
            admin = User(email="neuma.mindscape@gmail.com",
                         user_type="Administrator")
            db.session.add(admin)
            db.session.commit()

        # seed words
        language = Languages.query.filter_by(id="english").first()
        if not language:
            language = Languages(id="english", sample_size=0, mean_count=0)
            db.session.add(language)
            db.session.commit()

        # multi-language support should start here
        if not Words.query.filter_by(language="english").first(): # maybe problematic if you want to update words
            sample_size = 0
            word_count = 0
            max = 0
            min = 100000000 # infinity would be nice

            # Fill in word count and mean
            with open('./data/english_freq.csv', newline='') as csvfile:
                rows = csv.reader(csvfile, delimiter=',')
                next(rows) # skip the column names
                for word, count in rows:
                    count = int(count)
                    if count > max:
                        max = count
                    if count < min:
                        min = count

                    sample_size += count
                    word_count += 1
                    word = Words(id=word, language=language.id, count=count)
                    db.session.add(word)
            
            language.sample_size = sample_size
            language.mean_count = sample_size // word_count
            language.max_count = max
            language.min_count = min
            db.session.commit()

        # Seeding Erowid's chat
        if not Chats.query.filter_by(id=1).first():
            # Get the path to the data directory
            data_dir = os.path.join(os.path.dirname(__file__), 'data', 'erowid')

            # Iterate over the files in the data directory
            for filename in os.listdir(data_dir):
                # Check if the file is a JSON file
                if filename.endswith('.json'):
                    # Construct the full path to the JSON file
                    file_path = os.path.join(data_dir, filename)
                    id = int(filename.split('.')[0]) # the part before .json
                    
                    # Open the JSON file and load the data
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        
                        # Set up user 
                        user = User(email=data['meta'][0]['Author'], user_type="Contributor")
                        db.session.add(user)
                        db.session.commit()

                        # Set up chat
                        chat = Chats(id=id, user=user.id, flag=False, language="english", summary=data['experience'])
                        db.session.add(chat)
                        db.session.commit()

                        # Set up categories
                        for substance in data['substances']:
                            chat_category = Chats_Categories(chat=chat.id, 
                                                             dose=substance['Dose'], 
                                                             method=substance['Method'], 
                                                             substance=substance['Substance'], 
                                                             weight=data['meta'][0]['Body Weight'])
                            db.session.add(chat_category)
                            db.session.commit()
                        
            db.session.commit()

    return app
