"""
Defines controllers and utilities for experience/sentiment analysis.
Also handles vectorstores.
"""
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

# typing
from langchain_core.embeddings import Embeddings

import utils

def get_messages_as_documents(messages: list) -> list[Document]:
    """
    Return the messages stored in sql as Documents to be loaded into vectorstore
    @messages: list of objects returned by Messages.query
    @return: list of langchain Document
    """
    return [Document(text=message.text, metadata={ # the text is pretty arbitrary
        "message_id": message.id, # for clustering
        "chat_id": message.chat, # mostly to figure out whether messages are from the same chat
        "centroid-replacement": message.centroid,
    }) for message in messages]

def create_vectorstores(messages: list, llm_embedder:Embeddings, experiences: list=[]):
    """
    Load the message vectorstore with messages and the experience vectorstore with experience.
    Must be done after database is initialized.
    @messages: the list of message db objects
    @experiences: the list of experiences db objects. Defaults to empty (brand new)
    @return 
    """
    docs = get_messages_as_documents(messages)

    message_vectorstore = FAISS.from_documents(
        docs , llm_embedder
    )

    # Set up experiences for embedding
    id_embedding_tuple = [(exp.id, llm_embedder.embed_query(utils.get_message(exp.centroid))) for exp in experiences]

    exp_vectorstore = FAISS.from_embeddings(id_embedding_tuple, llm_embedder)
    return message_vectorstore, exp_vectorstore

def get_k_nearest(query, vectorstore, k) -> list[tuple[Document, float]]:
    """
    Query the k nearest documents to the embedding vector. Theoretically, messages that are similar will be clustered together.

    @embedding_vector: the ouput of llm_embedder.embed_query()
    @vectorstore: the vectorstore object. Designed to work with both message and experiences
    @k: the number of results
    @returns: a list of tuples of the form (Document, similarity score)
    """
    results = vectorstore.similarity_search_with_score(query, k)
    return results

def get_k_nearest_by_vector(embedding_vector, vectorstore, k) -> list[tuple[Document, float]]:
    """
    Query the k nearest documents to the embedding vector. Theoretically, messages that are similar will be clustered together.

    @embedding_vector: the ouput of llm_embedder.embed_query()
    @vectorstore: the vectorstore object. Designed to work with both message and experiences
    @k: the number of results
    @returns: a list of tuples of the form (Document, similarity score)
    """
    results = vectorstore.similarity_search_with_score_by_vector(embedding_vector, k)
    return results

def cluster_new_message(message, message_vstore: FAISS, exp_vstore: FAISS, similarity_threshold: float):
    """
    Handle the addition of a new message

    @message: the message object. Must already be committed to have a valid id
    @message_vstore: the vectorstore that handles messages
    @exp_vstore: the vectorstore that handles experiences
    @similarity_threshold: the threshold of similarity that, if surpassed, will result in a new cluster with this message as centre
    @returns: the message object with assigned experience, its id within the vectorstore and a boolean that determines if a new cluster must be created
    """
    # This way the llm is only called once
    message_embeddings = message_vstore.embeddings.embed_query(message.text)

    # add to vectorstore
    message_vstore.add_embeddings([(message.text, message_embeddings)], metadatas=[{
        "chat-id": message.chat_id
    }])

    # query closest cluster
    closest_exp_doc, similarity_score = get_k_nearest_by_vector(message_embeddings, exp_vstore, 1)[0]

    if similarity_score <= similarity_threshold: # inside this cluster
        # TODO: implement online k-means
        # TODO: cleanup centroid messages
        exp_id = int(closest_exp_doc.page_content)
        experience = utils.get_experience(exp_id)
        centroid_message = utils.get_message(experience.centroid)
        centroid_embeddings = exp_vstore.embeddings.embed_query(centroid_message.text)

        message.experience = exp_id
        return message, False
    else: # new cluster
        return message, True # message experience will be set by the sql handler

def new_experience(exp_id, message, exp_vstore:FAISS):
    """
    Introduce new experience to vectorstore
    """
    # thank god the embeddings are deterministic
    exp_vstore.add_embeddings([(exp_id, exp_vstore.embeddings.embed_query(message.text))])