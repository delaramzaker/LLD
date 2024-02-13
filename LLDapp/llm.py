import os
import openai
import sys
import datetime
from langchain.llms import OpenAI
from dotenv import load_dotenv, find_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor 
from langchain.vectorstores import Chroma, DocArrayInMemorySearch
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.document_loaders import PyPDFLoader, TextLoader






llm_name = None

import os

def process_uploaded_file(file):

    _ = load_dotenv(find_dotenv()) # read local .env file

    # Load PDF
    loaders = [
        # Duplicate documents on purpose - messy data
            PyPDFLoader(file),
    ]
    docs = []
    for loader in loaders:
        docs.extend(loader.load())
    # Split
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1500,
        chunk_overlap = 150
    )
    splits = text_splitter.split_documents(docs)
    # persist_directory = 'chromadb-storage'
    # !rm -rf ./docs/chroma  # remove old database files if any 

    embedding = OpenAIEmbeddings()
    
    vectordb = Chroma.from_documents(
        documents=splits,
        embedding=embedding,
        # persist_directory=persist_directory
    ) 

    
    
    current_date = datetime.datetime.now().date()
    if current_date < datetime.date(2023, 9, 2):
        llm_name = "gpt-3.5-turbo-0301"
    else:
        llm_name = "gpt-3.5-turbo"

    
    # persist_directory = 'chromadb-storage'
    embedding = OpenAIEmbeddings()
    # vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)


    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    retriever=vectordb.as_retriever()
    llm = ChatOpenAI(model_name=llm_name, temperature=0)
    qa = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=retriever,
        memory=memory
    )
    return qa


def answer_question(qa, question):
    # docs = vectordb.similarity_search(question,k=3)
    # len(docs)
    
    # qa_chain = RetrievalQA.from_chain_type(
    #     llm,
    #     retriever=vectordb.as_retriever()
    # )
    # result = qa_chain({"query": question})
    # return result["result"]


    result = qa({"question": question})
    return result['answer']
