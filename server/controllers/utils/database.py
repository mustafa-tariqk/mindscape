"""
Utilities functions. Most require app context to be called
"""
import models
import nltk

def get_chat_language(chat_id):
    """
    Does exactly as the name implies
    @chat_id: the id of the chat
    @return: The language associated with the chat
    """
    return models.Chats.query.get(chat_id).language

def get_chat_count():
    """
    Get the number of chats in the database
    @return: the number of chats
    """
    return models.Chats.query.count()

def get_experience(exp_id=None):
    """
    Get the experience database object
    @exp_id: the id of the experience. If None will return everything.
    @return: the associated database object
    """
    if not exp_id:
        return models.Experiences.query.all()
    else:
        return models.Experiences.query.get(exp_id)

def get_chat(chat_id=None):
    """
    Get the chat database object
    @chat_id: the id of the chat. If None will return everything
    @return: the associated database object
    """
    if not chat_id:
        return models.Chats.query.all()
    else:
        return models.Chats.query.get(chat_id)

def update_chat_exp(chat_id, exp_id):
    """
    Update the chat experience
    @chat_id: the id of the chat
    @exp_id: the id of the experience
    """
    chat = models.Chats.query.get(chat_id)
    chat.experience = exp_id
    models.db.session.commit() # makes the update

def update_chat_summary(chat_id, summary):
    """
    Update the chat summary
    @chat_id: the id of the chat
    @summary: the new summary
    """
    chat = models.Chats.query.get(chat_id)
    chat.summary = summary
    models.db.session.commit() # makes the update

def get_message(message_id):
    """
    Get the message database object
    @message_id: the id of the message
    @return: the associated database object
    """
    return models.Messages.query.get(message_id)

def get_all_chat_messages(chat_id):
    """
    Does exactly as the name implies
    @chat_id: the id of the chat.
    @return: A list of messages from the requested chat
    """
    return models.Messages.query.filter_by(chat=chat_id).order_by(models.Messages.time).all()

def get_stringify_chat(chat_id, exclude_ai_messages:bool=False, prune_stop_words:bool=False, lowercase: bool=False):
    """
    Returns all messages in the specified chat as a single string.
    @chat_id: the id of the chat. If set to None
    @exclude_ai_messages: defaults to true. whether to exclude meessages sent by the chatbot
    @return: A string containing the entire correspondence.
    """
    if not chat_id:
        language = 'english'
        chat_log = "Did you ever hear the tragedy of Darth Plagueis the Wise?\
                    I thought not. It's not a story the Jedi would tell you. \
                    It's a Sith legend. Darth Plagueis was a Dark Lord of the Sith, \
                    so powerful and so wise he could use the Force to influence \
                    the midichlorians to create life... \
                    He had such a knowledge of the dark side that he could even \
                    keep the ones he cared about from dying. \
                    The dark side of the Force is a pathway to many abilities \
                    some consider to be unnatural. He became so powerful... \
                    the only thing he was afraid of was losing his power, \
                    which eventually, of course, he did. \
                    Unfortunately, he taught his apprentice everything he knew, \
                    then his apprentice killed him in his sleep. \
                    Ironic, he could save others from death, but not himself."
    else:
        language = get_chat_language(chat_id)
        chat_log = ' '.join([message.text for message in get_all_chat_messages(chat_id) if (not exclude_ai_messages or message.chat_type == 'Human')])
        
    stop_words = [] # Only loaded if prune_stop_words is true
    if prune_stop_words:
        stop_words = nltk.corpus.stopwords.words(language)

    tokens = nltk.tokenize.word_tokenize(chat_log)

    filtered_chat_log = ' '.join(filter(
        lambda x: x.isalpha() and (not prune_stop_words or x.lower() not in stop_words),
        tokens
    ))
    
    if lowercase: filtered_chat_log = filtered_chat_log.lower()

    return filtered_chat_log

def get_word_weight(word, language="english"):
    """
    Calculate the weights for the given word
    @word: word to calculate weight for. Must be lowercase and does not contain special characters (language specific) or numbers
    @return: weight attributed to the word
    """
    language = models.Languages.query.filter_by(id=language).first()
    if not language:
        print("Language not initialized")
        return # fail state

    word = models.Words.query.filter_by(id=word).first()

    if not word: # use mean frequency
        return language.mean_count/language.sample_size
    else:
        return word.count/language.sample_size
    
