import os
import openai
import sys
from langchain.llms import OpenAI
from langchain.document_loaders import PyPDFLoader
from dotenv import load_dotenv, find_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor 
from langchain.vectorstores import Chroma 
from langchain.embeddings.openai import OpenAIEmbeddings


def process_uploaded_file(file):
    sys.path.append('../..')

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
    persist_directory = '/Users/delaram/MyLLM/chromadb-storage'
    # !rm -rf ./docs/chroma  # remove old database files if any 

    embedding = OpenAIEmbeddings()

    vectordb = Chroma.from_documents(
        documents=splits,
        embedding=embedding,
        persist_directory=persist_directory
    ) 

    def pretty_print_docs(docs):
        print(f"\n{'-' * 100}\n".join([f"Document {i+1}:\n\n" + d.page_content for i, d in enumerate(docs)]))
    # Wrap our vectorstore
    llm = OpenAI(temperature=0)
    compressor = LLMChainExtractor.from_llm(llm) 
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=vectordb.as_retriever(search_type = "mmr")
    ) 
    question = "wat zijn de benodigdheden?"
    compressed_docs = compression_retriever.get_relevant_documents(question)
    pretty_print_docs(compressed_docs)

def answer_question(question):

    import os
    import openai
    import sys
    import datetime
    from dotenv import load_dotenv, find_dotenv
    from langchain.vectorstores import Chroma
    from langchain.embeddings.openai import OpenAIEmbeddings
    from langchain.chat_models import ChatOpenAI
    from langchain.chains import RetrievalQA

    sys.path.append('../..')


    _ = load_dotenv(find_dotenv()) # read local .env file

    
    current_date = datetime.datetime.now().date()
    if current_date < datetime.date(2023, 9, 2):
        llm_name = "gpt-3.5-turbo-0301"
    else:
        llm_name = "gpt-3.5-turbo"

    
    persist_directory = '/Users/delaram/MyLLM/chromadb-storage'
    embedding = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
    
    docs = vectordb.similarity_search(question,k=3)
    len(docs)
    
    llm = ChatOpenAI(model_name=llm_name, temperature=0)
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectordb.as_retriever()
    )
    result = qa_chain({"query": question})
    return result["result"]


