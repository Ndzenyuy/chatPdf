import boto3
import streamlit as st
import os
import uuid

## s3_clinet
s3_client = boto3.client("s3")
BUCKET_NAME = os.getenv("BUCKET_NAME")

## Bedrock
from langchain_community.embeddings import BedrockEmbeddings

## Text Splitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

## Pdf Loader
from langchain_community.document_loaders import PyPDFLoader

## import FAISS
from langchain_community.vectorstores import FAISS

from botocore.config import Config

my_config = Config(region_name='us-east-1')  
bedrock_client = boto3.client(service_name="bedrock-runtime", config=my_config)
bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1", client=bedrock_client)

def get_unique_id():
    return str(uuid.uuid4())

folder_path="/tmp/"

## Load index
def load_index():
    s3_client.download_file(Bucket=BUCKET_NAME, Key="my_faiss.faiss", Filename=f"{folder_path}myfaiss.faiss")
    s3_client.download_file(Bucket=BUCKET_NAME, Key="my_faiss.pkl", Filename=f"{folder_path}myfaiss.pkl")

## Main method
def main():
    st.header("This is client site for chat with PDF using Bedrock, RAG etc")
    load_index()
    dir_list = os.listdir(folder_path)
    st.write(f"Files and Directories in {folder_path}")
    st.write(dir_list)

if __name__ == "__main__":
    main()
    