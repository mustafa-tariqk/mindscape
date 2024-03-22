import json

from controllers.utils import database, ai, vstore

def get_k_weighted_frequency(chat_id, k, exclude_ai_messages:bool=True):
    """
    Return the top k frequently seen words from a Chat session.
    Weights frequency based on established word distribution.
    @k: number of words to return
    @chat_id: id of chat session
    @exclude_ai_messages: defaults to true. whether to exclude meessages sent by the chatbot
    @return: dictionary formatted as {word: word_frequency}
    """
    print("Chat ID: ", chat_id)
    word_frequency = {}
    chat_log = database.get_stringify_chat(chat_id, exclude_ai_messages, True, True)
    if not chat_id:
        language = 'english'
    else:
        language = database.get_chat(chat_id).language

    language_data = database.get_language(language)

    sample_size = 0
    for word in chat_log.split(" "):
        sample_size += 1
        if word not in word_frequency:  # potential performance hog
            word_frequency[word] = 1
        else:
            word_frequency[word] += 1

    def weighted_freq(x):
        """Calculate the weights associated with the word's frequency"""
        word_data = database.get_word(x)
        # may need some tuning.
        if not word_data:  # Very very rare words, possibly names
            count_diff = language_data.max_count-language_data.min_count
        else:  # Detect rare descriptors
            count_diff = language_data.max_count - word_data.count

        freq_diff = count_diff/language_data.sample_size
        return freq_diff

    # Maybe ensure both
    def display(x):
        word_data = database.get_word(x)
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

def get_experience_data(chat_id, exp_vectorstore, k):
    """
    Get the global experience data with similarity
    @chat_id: the id of the chat
    @exp_vectorstore: the experience vectorstore
    @k: the number of experiences to return similarity for
    @return schema {
        "experiences": [{
            "name": "",
            "similarity": 0.0 // float, defaults to 0.0 if outside of top k
            "percentage": 0 // int in range [0, 100], percentage of submission with this experience
        }]
    }
    """
    chat = database.get_chat(chat_id)
    chat_vector = exp_vectorstore.embedding_function.embed_query(chat.summary)
    global_chat_count = database.get_chat_count()
    exp_docs, similarity_score = vstore.get_k_nearest_by_vector(chat_vector, exp_vectorstore, k)
    similarity_dict = {exp_docs[i].page_content: similarity_score[i] for i in range(len(exp_docs))}

    results = {
        "experiences": [
            {"name": exp.name,
             "similarity": similarity_dict[str(exp.id)] if str(exp.id) in similarity_dict else 0.0,
             "percentage": int(100*exp.count/global_chat_count)} for exp in database.get_experience()
        ]
    }

    # normalizing the percentage so that it adds up to 100
    total_percentage = sum([exp['percentage'] for exp in results['experiences']])
    
    # get experience index in results with lowest similarity that is not 0
    lowest_sim_index = 0
    for i in range(len(results['experiences'])):
        experiences = results['experiences'] # just to make the next line shorter
        if experiences[i]['similarity'] < experiences[lowest_sim_index]['similarity'] and experiences[i]['similarity'] > 0:
            lowest_sim_index = i

    # if the total percentage is not 100, add the difference to the experience with lowest similarity
    if total_percentage < 100:
        results['experiences'][lowest_sim_index]['percentage'] += 100 - total_percentage
    
    return results