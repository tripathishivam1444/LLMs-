import streamlit as st
from  streamlit_chat import message
from utils import *
import re

from dotenv import load_dotenv

import os 

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')


if "user_input" not in st.session_state:
    st.session_state['user_input'] = []
    
    
 
if "AI_responce" not in st.session_state:
    st.session_state['AI_responce'] = []

st.sidebar.header("Upload Data")

# """getting Pdf files"""
pdf_files = st.sidebar.file_uploader("Upload Pdfs" , type=['pdf'], accept_multiple_files = True)


# """Getting URLS"""
urls = st.sidebar.text_area("Enter  URL ",  height = 80)
url_pattern = re.compile(r'https?://\S+?(?=\s|$)')
url_list = url_pattern.findall(urls)

upload_button = st.sidebar.button("Upload Data")


if upload_button:
    if (pdf_files != []) & (url_list != []):

        for file, url in zip(pdf_files, url_list):
            st.sidebar.write(f"Extracting text from PDF file: {file.name}")
            all_pdf_docs = pdf_to_text(pdf_files)
            all_web_docs = web_data_loader(url_list)
        st.sidebar.success("Pdf Data saved into Chroma DataBase", icon= "✅")
        st.sidebar.success("Web Data saved into Chroma DataBase", icon= "✅")
        
                      
    elif pdf_files:
        all_pdf_docs = pdf_to_text(pdf_files)
        st.sidebar.success("Pdf Data saved into Chroma DataBase", icon= "✅")
        
            
    elif url_list : 
        all_web_docs = web_data_loader(url_list)
        st.sidebar.success("Web Data saved into Chroma DataBase", icon= "✅")
            
    else:
        st.sidebar.write("please add at least url or Pdf")



input_query = st.chat_input("input your Query ")

if input_query:
    answer = genrating_answer_from_db(input_query)

    st.session_state.AI_responce.append(input_query)
    st.session_state.user_input.append(answer)

    
    
message_history = st.empty()

if message_history:
    for i in range(len(st.session_state['user_input'])):
        
        message(st.session_state['AI_responce'][i], avatar_style="miniavs", is_user=True , key=str(i) + 'data_by_user') #["Alice", "Bob", "Charlie"]
        
        message(st.session_state["user_input"][i], key=str(i), avatar_style="icons")
    
    
