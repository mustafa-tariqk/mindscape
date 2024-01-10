import models
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFacePipeline

tokenizer = AutoTokenizer.from_pretrained(
    "microsoft/phi-2", trust_remote_code=True)
base_model = AutoModelForCausalLM.from_pretrained(
    "microsoft/phi-2", trust_remote_code=True)
pipe = pipeline("text-generation", model=base_model,
                tokenizer=tokenizer, max_new_tokens=100)
llm = HuggingFacePipeline(pipeline=pipe)


template = """respond to the instruction below. behave like a chatbot 
and respond to the user. try to be helpful.
### Instruction:
{instruction}
Answer:"""
prompt = PromptTemplate(template=template, input_variables=["instruction"])

llm_chain = LLMChain(prompt=prompt,
                     llm=llm,
                     )


def ai_message(id, message):
    conversation = models.Chats.query.get(id)
    return llm_chain.invoke(message)['text']


if __name__ == "__main__":
    print(llm_chain.invoke("hello")['text'])
