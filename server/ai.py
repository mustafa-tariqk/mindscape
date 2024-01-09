from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFacePipeline

tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2", trust_remote_code=True)
base_model = AutoModelForCausalLM.from_pretrained("microsoft/phi-2", trust_remote_code=True)
pipe = pipeline("text-generation", model=base_model, tokenizer=tokenizer)
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
question = "INTRODUCE YOURSELF"
print(llm_chain.run(question))

def ai_message(chat):
    output = "I am a robot"
    return output