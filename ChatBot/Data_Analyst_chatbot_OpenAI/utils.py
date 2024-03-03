# from langchain.agents import create_pandas_dataframe_agent
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_community.llms import OpenAI
import pandas as pd

def query_Agent(data, query):
    df = pd.read_csv(data)
    open_llm = OpenAI()
    
    agent = create_pandas_dataframe_agent(llm=open_llm, df= df , verbose=True)
    
    return agent.run(query)
 
 