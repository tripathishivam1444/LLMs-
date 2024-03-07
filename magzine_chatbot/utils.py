from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
# from langchain.vectorstores import Chroma
# from lagchain.llms.openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_community.vectorstores.chroma import  Chroma 
import streamlit as st
from langchain_community.document_loaders import UnstructuredURLLoader
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import VectorDBQAWithSourcesChain
# from Langchain.llms import 
from openai import  OpenAI

import os 
# os.environ['OPENAI_API_KEY'] = "OPENAI_API_KEY"
os.environ['OPENAI_API_KEY'] = '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'

import os

folder_name = "Vector_DB"

# Check if the folder already exists
if not os.path.exists(folder_name):
    # Create the folder if it doesn't exist
    os.makedirs(folder_name)
    print(f"Folder '{folder_name}' created successfully.")
else:
    print(f"Folder '{folder_name}' already exists.")



# #------------------------------------------------------------------------
# """LOad All the Pdf Data """

def pdf_to_text(pdf_files):
    all_pdf_text_list = []
    source_list = []
    for file in pdf_files:
        pdf = PdfReader(file)
        for page_number in range(len(pdf.pages)):
            page = pdf.pages[page_number]
            text = page.extract_text()
            all_pdf_text_list.append(text)
            source_list.append(file.name + "_page_" + str(page_number))
            
    text_splitter = RecursiveCharacterTextSplitter( )
    
    # vector_db = Chroma.from_texts(all_pdf_text_list, OpenAIEmbeddings())
    pdf_docs = text_splitter.create_documents(all_pdf_text_list, metadatas = [{"sounrce" : s} for s in source_list])
    
    st.write( "pdf_docs -------> ",pdf_docs)
    embeddings = OpenAIEmbeddings()
    pdf_chroma_db = Chroma.from_documents(pdf_docs, embedding=embeddings, persist_directory= "Vector_DB/")
    pdf_chroma_db.persist()
    return pdf_docs
    

# #-----------------------------------------------------------------------------------------------------
# """It Loads all the url  Data"""

def web_data_loader(urls ):
    web_data = WebBaseLoader(urls)
    web_text = web_data.load()
    # print("web Text ------------->", web_text)
    text_splitter = RecursiveCharacterTextSplitter()    
    
    web_docs = text_splitter.split_documents(web_text)
    st.write("web_docs -------------> ", web_docs)
    embeddings = OpenAIEmbeddings()
    web_chroma_db = Chroma.from_documents(web_docs,embedding=embeddings, persist_directory= "Vector_DB/")
    web_chroma_db.persist()
    return web_chroma_db
    
    

vector_Batabase = Chroma(persist_directory= "Vector_DB/", embedding_function=OpenAIEmbeddings())
# vector_BD = vector_Batabase.get()
# st.write("vector_BD ---> ", vector_BD)


# # ------------------------------------------------------------------------

def genrating_answer_from_db( query , vector_BD = vector_Batabase):

    model = ChatOpenAI(model = 'gpt-3.5-turbo-16k', temperature = 0.7)

    RAG = RetrievalQA.from_chain_type(llm = model , chain_type = 'refine', retriever = vector_BD.as_retriever())
    # RAG = VectorDBQAWithSourcesChain.from_chain_type(llm = OpenAI(),k = 1, chain_type= "stuff", vectorstore = vector_BD)
    # st.write(RAG)
    answer  = RAG.run(query)
    # answer  = RAG(str(query))
    return answer
    