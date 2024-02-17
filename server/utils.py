"""
Utilities functions.
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

def get_all_chat_messages(chat_id=None):
    """
    Does exactly as the name implies
    @chat_id: the id of the chat. Defaults to None. If not provided, get all messages.
    @return: A list of messages from the requested chat
    """
    if not chat_id:
        return models.Messages.query.order_by(models.Messages.time).all()
    else:
        return models.Messages.query.filter_by(chat=chat_id).order_by(models.Messages.time).all()

def get_stringify_chat(chat_id, exclude_ai_messages:bool=False, prune_stop_words:bool=False, lowercase: bool=False):
    """
    Returns all messages in the specified chat as a single string.
    @chat_id: the id of the chat
    @exclude_ai_messages: defaults to true. whether to exclude meessages sent by the chatbot
    @return: A string containing the entire correspondence.
    """
    language = get_chat_language(chat_id)
    chat_log = ""
    stop_words = [] # Only loaded if prune_stop_words is true
    if prune_stop_words:
        stop_words = nltk.corpus.stopwords.words(language)

    chat_log = ' '.join([message.text for message in get_all_chat_messages(chat_id) if (not exclude_ai_messages or message.chat_type == 'Human')])

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
    
