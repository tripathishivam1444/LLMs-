

import streamlit as st
from dotenv import load_dotenv
from utils import *



def main():
    
    load_dotenv()
    
    st.set_page_config(page_title="Invoice Extraction Bot")
    st.sidebar.text("Powered by U TRIPATHI 😎")
    st.title("Invoice Extraction Bot 🤖")
    
    all_pdf_files = st.file_uploader("Upload Your Invoice Pdf" , type = ["pdf"], accept_multiple_files = True)
    
    submit = st.button("Submit")

    
    if submit:
        df = pdf_to_DataFrame(all_pdf_files)
        
        st.write(df.head())
        
        data_to_csv = df.to_csv(index = False).encode("utf-8")
        
        st.download_button("Download Data as csv", data_to_csv, "invoice_extracted_data.csv", "text/csv", key = "download-tools-csv")
        
        st.success("Hope I was able to save your time")
        
if __name__ == '__main__':
    main()