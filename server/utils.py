"""
Utilities functions.
"""
import models

def get_all_chat_messages(chat_id):
    """
    Does exactly as the name implies
    @chat_id: the id of the chat
    @return: A list of messages from the requested chat
    """
    return models.Messages.query.filter_by(chat=chat_id).order_by(models.Messages.time).all()

def get_stringify_chat(chat_id, include_ai_messages:bool=True):
    """
    Returns all messages in the specified chat as a single string.
    @chat_id: the id of the chat
    @include_ai_messages: defaults to true. whether to include meessages sent by the chatbot
    @return: A string containing the entire correspondence.
    """
    chat_log = ""

    if not include_ai_messages:
        chat_log = ' '.join([message.text for message in get_all_chat_messages(chat_id) if message.chat_type == 'Human'])
    else:
        chat_log = ' '.join([message.text for message in get_all_chat_messages(chat_id)]) 

    filtered_chat_log = ''.join(filter(
        lambda x: x.isalpha() or x == ' ',  # ensure words are split properly
        chat_log
    )).lower()
    
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
    
