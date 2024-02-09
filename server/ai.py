""" 
This file contains the AI logic for the chatbot. 
It is responsible for generating responses to user messages. 
"""

import models
from dotenv import load_dotenv
from langchain.memory import ConversationKGMemory
from langchain_openai import OpenAI
from langchain.chains import ConversationChain
from langchain.prompts.prompt import PromptTemplate

load_dotenv()

llm = OpenAI()

template = """The following is a friendly conversation between a human and an AI. 
The AI is talkative and provides lots of specific details from its context. 
If the AI does not know the answer to a question, it truthfully says it does not know. 
The AI ONLY uses information contained in the "Relevant Information" section and does not hallucinate. 
Relevant Information: {history} 
Conversation: Human: {input} 
AI:"""

prompt = PromptTemplate(input_variables=["history", "input"], template=template)

conversation = ConversationChain(
    llm=llm, prompt=prompt, memory=ConversationKGMemory(llm=llm)
)


def ai_message(chat_id, message):
    """
    @chat_id: the id of the chat
    @message: the message to the AI
    @return: the response from the AI
    """
    session = models.Chats.query.get(chat_id)
    return conversation.predict(message)
