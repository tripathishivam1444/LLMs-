import streamlit as st
from dotenv import load_dotenv
from utils import *



def main():
    
    load_dotenv()
    
    st.set_page_config(page_title="Email Information Extraction Bot")
    st.sidebar.text("Powered by U TRIPATHI 😎")
    st.title("Email Information Extraction Bot 🤖")
    
    all_user_text = st.text_area("Insert Your text" )

    
    submit = st.button("Submit")
    # st.markdown("<iframe src='https://lottie.host/ec400ab0-25a6-460a-be73-54b953a34fe8/2NEoRYSJKN.json' width='300' height='500' scrolling='no'></iframe>", unsafe_allow_html=True)
    
    html_code1 = """
    <script src="https://unpkg.com/@dotlottie/player-component@latest/dist/dotlottie-player.mjs" type="module"></script>
    <dotlottie-player src="https://lottie.host/ec400ab0-25a6-460a-be73-54b953a34fe8/2NEoRYSJKN.json" background="transparent" speed="0.6" style="width: 300px; height: 300px;" loop autoplay></dotlottie-player>
    """

    # st.components.v1.html(html_code1, height=300)

    html_code2 = """
    <script src="https://unpkg.com/@dotlottie/player-component@latest/dist/dotlottie-player.mjs" type="module"></script> 

    <dotlottie-player src="https://lottie.host/3919d81a-d5c1-4df1-bc27-7bfb2af6c581/ZIwTqzqwvG.json" background="transparent" speed="0.4" style="width: 300px; height: 300px;" loop autoplay></dotlottie-player>"""
    
    # st.components.v1.html(html_code2, height=300)
    

    
    
    if submit:
        
        df = raw_data_to_information(all_user_text)
        
        st.write(df.head())
        
        data_to_csv = df.to_csv(index = False).encode("utf-8")
        
        # st.download_button("Download Data as csv", data_to_csv, "invoice_extracted_data.csv", "text/csv", key = "download-tools-csv")
        st.download_button("Download Data as csv", data_to_csv, file_name="Account_Data_extracted.csv", mime="text/csv", key="download-tools-csv")
        
        st.success("Hope I was able to save your time")
        
        
        
        
    col1, col2 = st.columns(2)

    # Display the HTML components in the columns
    with col1:
        st.components.v1.html(html_code1, height=400)

    with col2:
        st.components.v1.html(html_code2, height=400)
        
if __name__ == '__main__':
    main()
