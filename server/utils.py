"""
Utilities functions.
"""

import models

def get_all_chat_messages(chat_id):
    """
    Does exactly as the name implies
    @chat_id: the id of the chat
    @return: A list of string of messages from the requested chat
    """
    return models.Messages.query.filter_by(chat=chat_id).order_by(models.Messages.time).all()

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
    
