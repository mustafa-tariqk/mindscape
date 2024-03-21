""" 
This file contains the AI logic for the chatbot. 
It is responsible for generating responses to user messages. 
"""
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain.chains import ConversationChain, create_structured_output_runnable
from langchain.memory import ConversationKGMemory, ChatMessageHistory
from langchain.prompts.prompt import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain
from langchain_text_splitters import RecursiveCharacterTextSplitter

# new stuff
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


from controllers.utils.database import get_all_chat_messages, get_stringify_chat

# Load in the template
with open("data/template.txt", encoding="utf-8") as file:
    template = file.read()

try: # Setup LLM
    load_dotenv()
    llm_embedder = OpenAIEmbeddings()
    llm = ChatOpenAI(
        model_name='gpt-3.5-turbo-16k',
        temperature = 0.8,         
    )

    prompt = PromptTemplate(
        input_variables=["history", "input"],
        template=template
    )
except Exception as e: # Setup dummy text for testing/if API keys missing
    print(e)
    llm = None
    llm_embedder = None
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

def get_common_experience(documents: list[Document]) -> str:
    """
    From a list of messages that should contain common experiences, find the commonality between them.
    @documents: list of messages as Document
    @return: AI response
    """
    # TODO: make a prompt template

def categorize_submission(chat_id):
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
            "weight in kg": {"type": "integer"},
            "height in cm": {"type": "integer"},
            "substance": {"type": "string"}, # Possibly multiple
        }
    }
    # Define extractor
    runnable = create_structured_output_runnable(submission_schema, llm)
    # Fetch chat
    chat_log = get_stringify_chat(chat_id, True)

    # Extract from chat
    submission_info = runnable.invoke(chat_log)

    return submission_info

def summarize_submission(chat_id):
    """
    Summarizes the chat.
    @chat_id: the id of the chat
    @return: the summary
    """
    # Fetch chat as document
    chat_log = Document(get_stringify_chat(chat_id, True))


    # Split into chunks of 2000
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=2000, chunk_overlap=0
    )

    splits = splitter.split_documents([chat_log])

    # Map
    map_template = """The following is a set of documents
    {docs}
    Based on this list of docs, please identify the experiences being described. 
    Helpful Answer:"""
    map_prompt = PromptTemplate.from_template(map_template)
    map_chain = LLMChain(llm=llm, prompt=map_prompt)

    # Reduce, avoids clustering because of the substance name
    reduce_template = """The following is set of summaries:
    {docs}
    Take these and distill it into a final, consolidated summary of the experience being described.
    Do not mention the name of the substance being used. 
    Helpful Answer:"""
    reduce_prompt = PromptTemplate.from_template(reduce_template)
    # Run chain
    reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)

    # Takes a list of documents, combines them into a single string, and passes this to an LLMChain
    combine_documents_chain = StuffDocumentsChain(
        llm_chain=reduce_chain, document_variable_name="docs"
    )

    # Combines and iteratively reduces the mapped documents
    reduce_documents_chain = ReduceDocumentsChain(
        # This is final chain that is called.
        combine_documents_chain=combine_documents_chain,
        # If documents exceed context for `StuffDocumentsChain`
        collapse_documents_chain=combine_documents_chain,
        # The maximum number of tokens to group documents into.
        token_max=4000,
    )   

    # Combining documents by mapping a chain over them, then combining results
    map_reduce_chain = MapReduceDocumentsChain(
        # Map chain
        llm_chain=map_chain,
        # Reduce chain
        reduce_documents_chain=reduce_documents_chain,
        # The variable name in the llm_chain to put the documents in
        document_variable_name="docs",
        # Return the results of the map steps in the output
        return_intermediate_steps=False,
    )

    # Run chain
    return map_reduce_chain.invoke(splits)["output_text"]
