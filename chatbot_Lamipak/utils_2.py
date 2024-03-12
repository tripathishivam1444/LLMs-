from langchain.prompts import PromptTemplate
from langchain.document_loaders import WebBaseLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import SeleniumURLLoader
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
import nest_asyncio
from langchain_community.vectorstores.chroma import  Chroma 
import streamlit as st
from langchain_community.document_loaders import UnstructuredURLLoader
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import OpenAI
from dotenv import load_dotenv
import time 
from langchain_community.vectorstores import Qdrant
from langchain.vectorstores import Qdrant
from langchain.chains import RetrievalQA




import os 

# folder_name = "Vector_DB"

# # Check if the folder already exists
# if not os.path.exists(folder_name):
#     # Create the folder if it doesn't exist
#     os.makedirs(folder_name)
#     print(f"Folder '{folder_name}' created successfully.")
# else:
#     print(f"Folder '{folder_name}' already exists.")



#------------------------------------------------------------------------
"""LOad All the Pdf Data """

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
            
    text_splitter = RecursiveCharacterTextSplitter( chunk_size = 1000, chunk_overlap = 0, length_function = len,)
    
    # vector_db = Chroma.from_texts(all_pdf_text_list, OpenAIEmbeddings())
    pdf_docs = text_splitter.create_documents(all_pdf_text_list, metadatas = [{"sounrce" : s} for s in source_list])
    
    st.write( "pdf_docs -------> ",pdf_docs)
    
    url="https://0c48d6c0-91d3-48ae-95b9-414ed284aad7.us-east4-0.gcp.cloud.qdrant.io:6333", 
    api_key="JHbe2Onl9d7skuq9POOZgK3Zma_iJQu59zPtks7F0o9WrtAiKJcpcw",
    qdrant = Qdrant.from_documents(pdf_docs,
                                   OpenAIEmbeddings(api_key="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"), # api_key="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"
                                   url=url[0],
                                   prefer_grpc=True,
                                   api_key=api_key[0],
                                   collection_name="mycollection")
    
    # pdf_chroma_db = Chroma.from_documents(pdf_docs, embedding=embeddings, persist_directory= "Vector_DB/")
    # pdf_chroma_db.persist()
    return qdrant
    

# #-----------------------------------------------------------------------------------------------------
# """It Loads all the url  Data"""

def web_data_loader(urls):
    try:
        loader = SeleniumURLLoader(urls=urls)
        web_text = loader.load()
    except:
        st.write("SeleniumURLLoader Error Occurred ")
        print("\n\n ----------->> SeleniumURLLoader Error Occurred <<------------ \n\n ")
        try:
            web_data = WebBaseLoader(urls)
            web_text = web_data.load()
        except:
            st.write("WebBaseLoader Error Occurred ")
            print("\n\n --------->> WebBaseLoader Error Occurred <<--------- \n\n ")
            web_data = UnstructuredURLLoader(urls)
            web_text = web_data.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0, length_function=len)

    web_docs = text_splitter.split_documents(web_text)
    st.write("web_docs -------------> ", web_docs)

    # Assuming doc_content is the actual content of the document
    embeddings = OpenAIEmbeddings(api_key="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")

    # Creating a dummy class with page_content and metadata attributes
    class Document:
        def __init__(self, page_content, metadata):
            self.page_content = page_content
            self.metadata = metadata 

    # Iterate over each document and create Chroma database
    
    st.write(f"\n\n total ---> {len(web_docs)} documents are these \n\n ")
    st.write("\n\n Document Saving in DB ......\n\n " )
    for i, doc_content in enumerate(web_docs):
        # Creating a Document instance for each document
        document = Document(doc_content.page_content, doc_content.metadata)
        print(document)

        # Creating Chroma database from a single document
        web_chroma_db = Chroma.from_documents([document], embedding=embeddings, persist_directory="Vector_DB/")
        
        
        url="https://0c48d6c0-91d3-48ae-95b9-414ed284aad7.us-east4-0.gcp.cloud.qdrant.io:6333", 
        api_key="JHbe2Onl9d7skuq9POOZgK3Zma_iJQu59zPtks7F0o9WrtAiKJcpcw",
        qdrant = Qdrant.from_documents([document],
                               OpenAIEmbeddings(api_key="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"),
                               url=url[0],
                               prefer_grpc=True,
                               api_key=api_key[0],
                               collection_name="mycollection")
        
        st.write( f"{i}/{len(web_docs)}" )
        time.sleep(25)
    return qdrant



from langchain_openai import OpenAIEmbeddings
import qdrant_client
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Qdrant
from langchain_community.llms import OpenAI

url="https://0c48d6c0-91d3-48ae-95b9-414ed284aad7.us-east4-0.gcp.cloud.qdrant.io:6333"
api_key="JHbe2Onl9d7skuq9POOZgK3Zma_iJQu59zPtks7F0o9WrtAiKJcpcw"
    
embeddings = OpenAIEmbeddings(api_key= "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" )
client = qdrant_client.QdrantClient(  url=url, prefer_grpc=True, api_key=api_key)

vectorstore = Qdrant(
        client=client,
        collection_name= 'mycollection',
        embeddings=embeddings
    )

# vector_BD = vector_Batabase.get()
# st.write("vector_BD ---> ", vector_BD)


# # ------------------------------------------------------------------------

def genrating_answer_from_db( query , vectorstore =  vectorstore):  #vector_BD = vector_Batabase

    # model = ChatOpenAI(model = 'gpt-3.5-turbo-16k', temperature = 0.7)
    # template = """
    #                 you have to genrate or create answer only from given context.
    #                 Rule: develop this quetion answer from this context.
    #                 Rule: Don't try to say 'I don't know the answer' or don't try to escape the Question. you have to give as much as posible answer from this given context.
    #                 Rule: You should develop answer from this contxt.
    #                 Context: {context}
    #                 Question: {question}
    #                 Answer: """ 
                    
    #                 Rule: You are not suppose to give answer yo own.
    #                 any word and any Question word are littile bit similar thank you should have give answer based on context.
    #                 if any question word and any context word are not simmilar than you just say, 'I am less aware of 🙄 what you are asking, please Increase my knowlege 📚 by uploadfing pdf, OR just website/YouTube video links.🙂'  


    # prompt = PromptTemplate(template=template, input_variables = ["context", "question"])
    # rag_chain = (
    #             {"context": vector_BD.as_retriever(),  "question": RunnablePassthrough()} 
    #             | prompt 
    #             | model
    #             | StrOutputParser() 
    
    # print("vectorstore-->", vectorstore)
    qa = RetrievalQA.from_chain_type(llm=OpenAI(api_key = "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" ),
                                chain_type="stuff",
                                retriever=vectorstore.as_retriever() )
    #             )
    answer = qa.run(query)
    return answer






# print("\n\n qa ----->>  ", qa)
# print(f"\n\n\n ------> {qa.run("what milk production in india?")}")
    


    