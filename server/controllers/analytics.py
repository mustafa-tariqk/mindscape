from flask import jsonify

from server.controllers.utils import wordcloud, database, ai

def get_wordcloud_data(chat_id, k):
    """
    Get the wordcloud data for the chat
    @chat_id: the id of the chat
    @k: the number of words to return
    @return schema {
        'global_count': frequency in language distribution,
        'local_count': frequency in chat,
        'global_max - global_count': difference from the most used word,
        'weight': attributed weight
    }
    """
    return jsonify(wordcloud.get_k_weighted_frequency(k, chat_id))

def get_experience_data(chat_id):
    """
    Get the global experience data with similarity
    @chat_id: the id of the chat
    @return schema {
        "experiences": [{
            "name": "",
            "similarity": 0.0 // float 
            "percentage": 0 // int in range [0, 100], percentage of submission with this experience
        }]
    }
    """
    chat = database.get_chat(chat_id)
    return jsonify({
        "experiences": [{
            "name": "Infinite Power",
            "similarity": 300.0,
            "percentage": 20
        }, {
            "name": "Signature Look of Authority",
            "similarity": 100.0,
            "percentage": 30
        }, {
            "name": "I am your father",
            "similarity": 50.0,
            "percentage": 50
        }]
    })