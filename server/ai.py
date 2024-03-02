""" 
This file contains the AI logic for the chatbot. 
It is responsible for generating responses to user messages. 
"""
from dotenv import load_dotenv
from langchain.chains import ConversationChain, create_structured_output_runnable
from langchain.memory import ConversationKGMemory, ChatMessageHistory
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import OpenAI

from utils import get_all_chat_messages, get_stringify_chat

# Load in the template
with open("data/template.txt", encoding="utf-8") as file:
    template = file.read()

try: # Setup LLM
    load_dotenv()
    llm = OpenAI()
    prompt = PromptTemplate(
        input_variables=["history", "input"],
        template=template
    )
except Exception as e: # Setup dummy text for testing/if API keys missing
    llm = None
    prompt = None

def ai_message(chat_id, human_message):
    """
    @chat_id: the id of the chat
    @message: the message to the AI
    @return: the response from the AI
    """
    if llm is None or prompt is None:
        return "API Keys not found."

    # Collect message history
    messages = get_all_chat_messages(chat_id)

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
    ).predict(input=human_message)


def handle_submission(chat_id):
    """
    Verifies that there is enough information for submission and categorize accordingly.
    Flag submissions without enough information. 
    @chat_id: the id of the chat
    @app: the flask app to get the app context
    """
    # Defines schema for extraction, add more in template
    submission_schema = {
        "type": "object",
        "properties": {
            "weight": {"type": "integer"},
            "height": {"type": "integer"},
            "substance": {"type": "string"}, # Possibly multiple
        }
    }
    # Define extractor
    runnable = create_structured_output_runnable(submission_schema, llm)
    # Fetch chat
    chat_log = get_stringify_chat(chat_id, True)

    # Extract from chat TODO: add to database
    submission_info = runnable.invoke(chat_log)

    return submission_info