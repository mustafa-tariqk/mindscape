from server.controllers.utils import wordcloud, database, ai, vstore


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
    return wordcloud.get_k_weighted_frequency(k, chat_id)

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
    chat_vector = ai.embed_query(chat.summary)
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