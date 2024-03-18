"""
This file handles the calculation necessary to support the wordcloud frontend as part of analytics.
Uses the frequency files in data. This frequency file will also determine the language used.
"""
import json

import utils
import models


def get_k_weighted_frequency(k, chat_id, exclude_ai_messages:bool=True, test=False):
    """
    Return the top k frequently seen words from a Chat session.
    Weights frequency based on established word distribution.
    @k: number of words to return
    @chat_id: id of chat session
    @exclude_ai_messages: defaults to true. whether to exclude meessages sent by the chatbot
    @return: dictionary formatted as {word: word_frequency}
    """
    word_frequency = {}
    if test:
        chat_log = utils.get_stringify_chat(chat_id, exclude_ai_messages, True, True)
        language = utils.get_chat_language(chat_id)
    else: # easter egg
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
        language = 'english'
    language_data = models.Languages.query.get(language)

    sample_size = 0
    for word in chat_log.split(" "):
        sample_size += 1
        if word not in word_frequency:  # potential performance hog
            word_frequency[word] = 1
        else:
            word_frequency[word] += 1

    def weighted_freq(x):
        """Calculate the weights associated with the word's frequency"""
        word_data = models.Words.query.get(x)
        # may need some tuning.
        if not word_data:  # Very very rare words, possibly names
            count_diff = language_data.max_count-language_data.min_count
        else:  # Detect rare descriptors
            count_diff = language_data.max_count - word_data.count

        freq_diff = count_diff/language_data.sample_size
        return freq_diff

    # Maybe ensure both
    def display(x):
        word_data = models.Words.query.get(x)
        global_count = 0
        weight = 0

        if not word_data:  # Very very rare words, possibly names
            global_count = language_data.min_count
        else:  # Detect rare descriptors
            global_count = word_data.count

        weight = (language_data.max_count - global_count)/language_data.sample_size

        data = {
            'global_count': global_count,
            'local_count': word_frequency[x],
            'global_max - global_count': language_data.max_count - global_count,
            'weight': weight
        }
        return data

    unique_words = list(word_frequency.keys())
    # sort in descending order based on weighted frequency
    unique_words.sort(reverse=True, key=weighted_freq)
    # Return the top k
    return json.dumps({x: display(x) for x in unique_words[0:k]}, indent=4)