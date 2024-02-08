"""
This file contains the AI logic for the chatbot. It is responsible for 
generating responses to user messages.
"""
import torch
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import models

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


TEMPLATE = """respond to the instruction below. behave like a chatbot
and respond to the user. try to be helpful.
### Instruction:
{instruction}
Answer:"""  # future: change this template to be more helpful

prompt = PromptTemplate(template=TEMPLATE, input_variables=["instruction"])
llm_chain = LLMChain(
    prompt=prompt,
    llm=llm,
)


def ai_message(chat_id, message):
    """
    @chat_id: the id of the chat
    @message: the message to the AI
    @return: the response from the AI
    """
    conversation = models.Chats.query.get(chat_id)
    print(conversation)
    # future: implement entire conversation into chain. very cool
    return llm_chain.invoke(message)["text"]
