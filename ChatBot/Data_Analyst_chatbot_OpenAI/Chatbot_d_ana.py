pip install -r .\requirenments.txt
import streamlit as st
#from dotenv import load_dotenv
from utils import *
from streamlit_chat import message

load_dotenv()

st.title("U TRIPATHI Data Analysis chatbot for CSV files.")

if 'user_input' not in st.session_state:
    st.session_state['user_input'] = []
 
if 'Chatbot_Responce' not in st.session_state:
    st.session_state['Chatbot_Responce'] = []

# Capture the CSV file
data = st.file_uploader("Upload your CSV file", type="csv")

# query = st.chat_input("Enter Your Query ")
# button = st.button("Generate Response ")


# if  query:
#     answer = query_Agent(data, query)
#     answer = answer.lstrip("\n")
#     st.session_state.Chatbot_Responce.append(query)
#     st.session_state.user_input.append(answer)
    
# messege_history = st.empty()

# if st.session_state['user_input'] :
#     for i in  range(len(st.session_state['user_input']), -1, -1, -1):
#         message(st.session_state['user_input'][i], key = str(i), avatar_style= "identicon")
#         message(st.session_state['Chatbot_Responce'][i], key = str(i)+ "data_by_user", avatar_style= "miniavs", is_user= True)
    

if 'user_input' not in st.session_state:
    st.session_state['user_input'] = []
 
if 'openai_response' not in st.session_state:
    st.session_state['openai_response'] = []
 

 
user_input = st.chat_input("write your query?")
 
if user_input:
    output = query_Agent(data, user_input)
    output = output.lstrip("\n")
 
    # Store the output
    st.session_state.openai_response.append(user_input)
    st.session_state.user_input.append(output)
 
message_history = st.empty()
 
with message_history.container(): 
    for i in range(len(st.session_state['user_input']) ):
        # This function displays OpenAI response
        
        message(st.session_state['openai_response'][i],
         avatar_style="initials", seed="Utkarsh", is_user=True,
        key=str(i) + 'data_by_user')
        
        
        message(st.session_state["user_input"][i],
                key=str(i),  avatar_style="initials", seed="AI")   #fun-emoji"
        # This function displays user input
