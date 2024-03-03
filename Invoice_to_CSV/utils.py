import pandas as pd
from PyPDF2 import PdfReader
import os
import regex as re
from openai import OpenAI
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import streamlit as st

os.getenv('OPENAI_API_KEY')

def pdf_reader(pdf_file):
    pdf = PdfReader(pdf_file)
    pdf_text = ""
    for text in pdf.pages:
        pdf_text += text.extract_text()
        
    return pdf_text

def get_data_from_AI(pdf_text):
    
    tempalte = """Extract all the Following Values : Invoice No., Discription, Quantity, Date, 
                    Unit Price, Amount, Total, Email, mobile no and Address from this data : {pdf_text}
                    
                    Rule: You Do not forget any spelling, punctuation, indentation marks. add them properly 
                    in output.
                    Rule: If You think some values are missing fill by None .
                    
                    This is Output Example for Reference: {{'Invoice No.' : 3424523, 'Discription' : 'office chair',
                    'Quantity': '32', 'Date': '3-Feb-2024' , 'Unit Price' : 423, 'Amount' : 3534 , 'Total':'323434',
                    'Email': 'shivan342@gmail.com, 'mobile no': '70211996042' : 'Address': 'L.B.S. Navpada, kurla, mumbai-400023' }}"""
                    
                     
    promp_template =  PromptTemplate(input_variables= ['pdf_text'], template = tempalte)
    llm = OpenAI(temperature = 0.7)
    
    full_responce = llm(promp_template.format(pdf_text = pdf_text))
    
    return full_responce
    
    
def pdf_to_DataFrame(all_pdf_files):
    
    df = pd.DataFrame({'Invoice No.' : pd.Series(dtype = 'str'),
                       'Discription': pd.Series(dtype = 'str'),
                       'Quantity' : pd.Series(dtype = 'str'),
                       'Date': pd.Series(dtype = 'str'),
                       'Unit Price': pd.Series(dtype = 'str'),
                       'Amount' : pd.Series(dtype = 'str'),
                       'Total': pd.Series(dtype = 'str'),
                       'Email' : pd.Series(dtype = 'str'),
                       'Mobile no': pd.Series(dtype = 'str'),
                       'Address' : pd.Series(dtype = 'str')})
    
    for i, file in enumerate(all_pdf_files):
        pdf_texts = pdf_reader(file)
        print("this is All Pdf RAW data ----> ", pdf_texts)

        AI_responce = get_data_from_AI(pdf_texts)
        print("This is AI REsponce Data ----> ", AI_responce)
        
        patten = r'{(.+)}'
        match = re.search(patten , AI_responce, re.DOTALL)
        print("match =======>>> ", match, "\n\n\n")
        
        if match:
            extracted_text = match.group(1)
            print("extracted Data ---> \n" , extracted_text)
            
            data_dict = eval('{' + extracted_text + '}')
            print("Data_dict -->  \n" ,data_dict)
            
        else:
            print("No match found ")
            
        data = pd.DataFrame(data_dict, index = [0])
            
        df = pd.concat([df, data], ignore_index = True)
        
        print("------------------------- ALL Done------------------------")
        
        st.write(f"{i + 1} pdf Done ")
        
    df.head()
    
    return df
        
        