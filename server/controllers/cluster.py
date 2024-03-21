from server.controllers import wordcloud
from utils import database, ai, vstore

def cluster_all_chats(k):
    """
    Cluster every single chat into its appropriate experience. Uses naive k-means.
    Data and time intensive. Meant for infrequent use.
    @k: the number of clusters
    @return: None
    """
    chats = database.get_chat() # get everything
    done = False # check for convergence

    # assign centroids. can be upgrade to k-means++
    centroids = [chats[i].id for i in range(k)]

    # Set up experiences for embedding
    id_embedding_tuple = [(exp, ai.llm_embedder.embed_query(database.get_message(chats[exp].summary))) for exp in centroids]

    while (not done):
        done = True

