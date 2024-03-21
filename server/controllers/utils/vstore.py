"""
Defines controllers and utilities for experience/sentiment analysis.
Also handles vectorstores.
"""
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

# typing
from langchain_core.embeddings import Embeddings

import server.controllers.utils.database as database

def get_messages_as_documents(messages: list) -> list[Document]:
    """
    Return the messages stored in sql as Documents to be loaded into vectorstore
    @messages: list of objects returned by Messages.query
    @return: list of langchain Document
    """
    return [Document(text=message.text, metadata={ # the text is pretty arbitrary
        "message_id": message.id, 
        "chat_id": message.chat, # mostly to figure out whether messages are from the same chat
    }) for message in messages]

def get_chats_as_documents(chats: list) -> list[Document]:
    """
    Return the chats stored in sql as Documents to be loaded into vectorstore
    @chats: list of objects returned by Chats.query
    @return: list of langchain Document
    """
    return [Document(text=chat.summary, metadata={
        "chat_id": chat.id, # for clustering
    }) for chat in chats]

def create_exp_vectorstore(experiences: list, llm_embedder:Embeddings):
    """
    Load the experience vectorstore with experience.
    @experiences: the list of experiences db objects.
    @return 
    """
    # Set up experiences for embedding
    id_embedding_tuple = [(exp.id, llm_embedder.embed_query(database.get_message(exp.centroid))) for exp in experiences]

    # Vector store will return the id of the matched experience
    exp_vectorstore = FAISS.from_embeddings(id_embedding_tuple, llm_embedder)
    return exp_vectorstore

def create_chats_vectorstore(chats: list, llm_embedder:Embeddings):
    """
    Load the chat vectorstore with chats.
    @chats: the list of chats db objects.
    @return 
    """
    # Set up chats for embedding
    id_embedding_tuple = [(chat.id, llm_embedder.embed_query(chat.summary)) for chat in chats]

    # Vector store will return the id of the matched chat
    chat_vectorstore = FAISS.from_embeddings(id_embedding_tuple, llm_embedder)
    return chat_vectorstore

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

def cluster_new_chat(chat, exp_vstore: FAISS):
    """
    Handle the addition of a new chat

    @chat: the chat object. Must already be committed to have a valid id
    @exp_vstore: the vectorstore that handles experiences
    @similarity_threshold: the threshold of similarity that, if surpassed, will result in a new cluster with this chat as centre
    @returns: the id of the cluster that the chat was added to, as well as similarity
    """
    # This way the llm is only called once
    chat_embeddings = exp_vstore.embeddings.embed_query(chat.summary)

    # query closest cluster
    return get_k_nearest_by_vector(chat_embeddings, exp_vstore, 1)[0]
