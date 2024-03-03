import streamlit as st
from dotenv import load_dotenv
from utils import query_Agent

load_dotenv()

st.title("U TRIPATHI Data Analysis platform for CSV file.")
st.header("u can upload CSV data file hare: ")

#capture the CSV file
data = st.file_uploader("upload your CSV file", type = "csv")

query = st.text_area("Enter Your Query ")
button = st.button("Genrate Responce ")

if button :
    answer = query_Agent(data, query)
    st.write(answer)
    


#------------------------------------------------------------------------------------------------    
"""Example Querys """

# how may diffrent columns are their in Data, give name of each columns and give sum od iffrent categories present in data