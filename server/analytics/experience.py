"""
Defines controllers and utilities for experience/sentiment analysis.
Also handles vectorstores.
"""
from langchain_core.documents import Document
from langchain_community.vectorstores import faiss # vectorestore

from ai import llm_embedder
import utils

def get_messages_as_documents(messages: list) -> list[Document]:
    """
    Return the messages stored in sql as Documents to be loaded into vectorstore
    @messages: list of objects returned by Messages.query
    @return: list of langchain Document
    """
    return [Document(text=messages.text, metadata={
        "chat_id": messages.chat # Mostly to figure out whether messages are from the same chat
    })]

def create_vectorstore(messages):
    """
    ONLY run after models.create_app().
    Load the vectorstore with messages.
    """
    vectorstore = faiss.from_documents(
        get_messages_as_documents(messages), llm_embedder
    )
    return vectorstore

def get_k_nearest_messages(vectorstore, k, embedding_vector):
    results = vectorstore.similarity_search_by_vector(embedding_vector)


