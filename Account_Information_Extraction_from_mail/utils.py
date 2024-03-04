import pandas as pd
import os
import regex as re
from openai import OpenAI
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import streamlit as st
import ast

os.getenv('OPENAI_API_KEY')



def get_data_from_AI(all_text):
    
    tempalte = """Extract all the Following Values : Account Name, Mobile No, Account Number, 
                IFSC No, Customer ID, MICS Code, Email ID and Address from this data : {all_text}
                    
                Rule: You Do not forget any spelling, punctuation, indentation marks. add them properly 
                in output.
                Rule: If You think some values are missing fill by None.
                Rule : In Output you should not include this 1: dictionary, 2: dictioary,  Person 2: Priya Sharma, Person 1: radha Sharma
                Rule : I want only Dictionary or Dictionaries in output. number or Dictionary will be Equal to number no of peoples details .
                This is 1 Example for Reference: {{'Account Name' : "Hanuman prajapati", 'Mobile No' : '7021246953',
                'Account Number': '07644536790525' , 'IFSC No' : 'BARB0DGVXDO', 'Customer ID' : 'FTB006754',
                'MICS Code' : '500056860', 'Email ID': 'shuvarmyvcs3498@gmail.com', 'Address' : "34/66, L.b.s. road, navpada kurla, west mumbai - 400070." }}
                
                This is 2 Example for Reference: {{'Account Name' : "hemant singh", 'Mobile No' : '7053246953',
                'Account Number': '07644683790525' , 'IFSC No' : 'BARB0DG1DDO', 'Customer ID' : 'FTB006764',
                'MICS Code' : '500056570', 'Email ID': 'shuvar3498@gmail.com', 'Address' : "34/66, L.b.s. road, Nerul, Navi Mumbai - 400070." }}"""
                    


    promp_template =  PromptTemplate(input_variables= ['all_text'], template = tempalte)
    llm = OpenAI(temperature = 0.7)
    
    full_responce = llm(promp_template.format(all_text = all_text))
    
    return full_responce
    


def raw_data_to_information(all_text):
    df = pd.DataFrame({
        'Account Name': pd.Series(dtype='str'),
        'Mobile No': pd.Series(dtype='str'),
        'Account Number': pd.Series(dtype='str'),
        'IFSC No': pd.Series(dtype='str'),
        'Customer ID': pd.Series(dtype='str'),
        'MICS Code': pd.Series(dtype='str'),
        'Email ID': pd.Series(dtype='str'),
        'Address': pd.Series(dtype='str')
    })

    AI_responce = get_data_from_AI(all_text)
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
        
    # data = pd.DataFrame(extracted_text, index = [0])
    data = pd.DataFrame.from_dict([data_dict])
    # df = pd.concat([df, data], ignore_index = True)
    
    print("------------------------- ALL Done------------------------")
    
    # st.write(f"{i + 1} pdf Done ")
        
    data.head()
    
    return data