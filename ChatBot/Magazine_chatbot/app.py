
import streamlit as st
#import accelerate
#from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from transformers import AutoTokenizer, FalconForCausalLM, AutoModelForCausalLM
import transformers
import torch

# from llama_index import LangchainEmbedding, ServiceContext
# from llama_index import SimpleInputPrompt
# from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
# from llama_index.llms import HuggingFaceLLM
# from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, ServiceContext # LLMPredictor, PromptHelper,
# from langchain.llms.openai import OpenAI



model = "tiiuae/falcon-7b-instruct"

falcon_tokenizer = AutoModelForCausalLM.from_pretrained(model, device_map="auto", load_in_4bit=True)  #,  use_auth_token=auth_token
falcon_tokenizer = AutoTokenizer.from_pretrained(model)
st.title("Evrything setup done 9GB model Downloaded")
