"""
This file handles the calculation necessary to support the wordcloud frontend as part of analytics.
Uses the frequency files in data. This frequency file will also determine the language used.
"""
import utils
import models

def get_k_weighted_frequency(k, chat_id):
    """
    Return the top k frequently seen words from a Chat session.
    Weights frequency based on established word distribution.
    @k: number of words to return
    @chat_id: id of chat session
    @return: dictionary formatted as {word: word_frequency}
    """
    word_frequency = {}
    chat_log = filter(
        lambda x: x.isalpha() or x == ' ', # ensure words are split properly
        utils.get_all_chat_messages(chat_id).join(' ')
    ).lower() # whole chat as a collection of words
    language = 'english' # TODO: provide default value of english for Chat property to be used here
    for word in chat_log.split(" "):
        if word not in word_frequency.keys():
            word_frequency[word] = 1
        else:
            word_frequency[word] += 1

    def weighted_freq(word):
        word_data = models.Words.query.get(word)
        language_data = models.Languages.query.get(language)
        # may need some tuning
        # sampled frequency * (1 / distribution probability)
        if not word_data:
            return word_frequency[word] * (language_data.sample_size / language_data.mean_count)
        else:
            return word_frequency[word] * (language_data.sample_size / word_data.count)

    unique_words = word_frequency.keys()
    unique_words.sort(reverse=True, key=weighted_freq) # sort in descending order based on weighted frequency
    return {x : word_frequency[x] for x in unique_words[0:k]} # Return the top k
        