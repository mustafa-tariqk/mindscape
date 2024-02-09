""" 
This file contains the AI logic for the chatbot. 
It is responsible for generating responses to user messages. 
"""
from dotenv import load_dotenv
from langchain.chains import ConversationChain
from langchain.memory import ConversationKGMemory, ChatMessageHistory
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import OpenAI

from models import Messages

# Load in template
with open("data/template.txt", encoding="utf-8") as file:
    template = file.read()

# Setup LLM
load_dotenv()
llm = OpenAI()
prompt = PromptTemplate(
    input_variables=["history", "input"],
    template=template
)

def ai_message(chat_id, human_message):
    """
    @chat_id: the id of the chat
    @message: the message to the AI
    @return: the response from the AI
    """
    # Collect message history
    messages = Messages.query.filter_by(chat=chat_id).order_by(Messages.time).all()

    # Transform data for langchain useage
    chat_memory = ChatMessageHistory()
    for message in messages:
        if message.chat_type == "AI":
            chat_memory.add_ai_message(message.text)
        else:
            chat_memory.add_user_message(message.text)

    # Generate output
    return ConversationChain(
        llm=llm,
        prompt=prompt,
        memory=ConversationKGMemory(llm=llm, chat_memory=chat_memory)
    ).predict(human_message)
