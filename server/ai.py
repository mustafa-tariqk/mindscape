""" 
This file contains the AI logic for the chatbot. 
It is responsible for generating responses to user messages. 
"""
<<<<<<< HEAD
<<<<<<< HEAD
This file contains the AI logic for the chatbot. It is responsible for 
generating responses to user messages.
"""
import torch
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
=======
=======
from dotenv import load_dotenv
from langchain.chains import ConversationChain
from langchain.memory import ConversationKGMemory
from langchain.prompts.prompt import PromptTemplate
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_openai import OpenAI
>>>>>>> 7089197 (stylefixes)

>>>>>>> 51bd514 (added memory)
import models

<<<<<<< HEAD
# Model too big for GPU
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2", trust_remote_code=True)
base_model = AutoModelForCausalLM.from_pretrained(
    "microsoft/phi-2", trust_remote_code=True
)
pipe = pipeline(
    "text-generation", model=base_model, tokenizer=tokenizer, max_new_tokens=100
) # Device to gpu if possible
llm = HuggingFacePipeline(pipeline=pipe)
=======
load_dotenv()
>>>>>>> 51bd514 (added memory)

llm = OpenAI()

TEMPLATE = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. 
If the AI does not know the answer to a question, it truthfully says it does not know. The AI ONLY uses information contained in the "Relevant Information" section and does not hallucinate.

Relevant Information:

{history}

Conversation:
Human: {input}
AI:"""


prompt = PromptTemplate(input_variables=["history", "input"], template=TEMPLATE)


def ai_message(chat_id, message):
    """
    @chat_id: the id of the chat
    @message: the message to the AI
    @return: the response from the AI
    """
    session = models.Chats.query.get(chat_id)

    chat_memory = BaseChatMessageHistory()

    return ConversationChain(
        llm=llm,
        prompt=prompt,
        memory=ConversationKGMemory(llm=llm, chat_memory=chat_memory),
    ).predict(message)
