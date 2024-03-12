import streamlit as st
from  streamlit_chat import message
# from utils import *
from utils_2 import  *
# from urls_extracter import *
from url_extractor_main import *
import re



if "user_input" not in st.session_state:
    st.session_state['user_input'] = []
    
    
 
if "AI_responce" not in st.session_state:
    st.session_state['AI_responce'] = []

st.sidebar.header("Upload Data")

# """getting Pdf files"""
pdf_files = st.sidebar.file_uploader("Upload Pdfs" , type=['pdf'], accept_multiple_files = True)

url_container = st.sidebar.text_area("paste yor link ")
# """Getting URLS"""
# all_


upload_button = st.sidebar.button("Upload Data")


if upload_button:
    
    visited_urls = set()
    all_urls = []

    url_pattern = re.compile(r'https?://\S+?(?=\s|$)')
    url_list = url_pattern.findall(url_container)

    for url in url_list:
        print("URL ---> ", url)
        home_page_url = get_home_page_url(url)

        list_of_urls = get_unique_urls(home_page_url, visited_urls)
        all_urls.extend(list_of_urls)
    
    

    
    if (pdf_files != []) & (all_urls != []):

        for file, url in zip(pdf_files, all_urls):
            st.sidebar.write(f"Extracting text from PDF file: {file.name}")
            all_pdf_docs = pdf_to_text(pdf_files)
            all_web_docs = web_data_loader(all_urls)
        st.sidebar.success("Pdf Data saved into Chroma DataBase", icon= "✅")
        st.sidebar.success("Web Data saved into Chroma DataBase", icon= "✅")
        
                      
    elif pdf_files:
        all_pdf_docs = pdf_to_text(pdf_files)
        st.sidebar.success("Pdf Data saved into Chroma DataBase", icon= "✅")
        
            
    elif all_urls : 
        all_web_docs = web_data_loader(all_urls)
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
    
    