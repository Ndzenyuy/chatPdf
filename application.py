import boto3
import streamlit as st
import os
import uuid

## s3_clinet
s3_client = boto3.client("s3")
BUCKET_NAME = os.getenv("BUCKET_NAME")

## Bedrock
from langchain_community.embeddings import BedrockEmbeddings
from langchain.llms.bedrock import Bedrock

from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

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


## Split the pages / text into chunks
def split_text(pages, chunk_size, chunk_overlap):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_splitter.split_documents(pages)
    return docs

## Create vector store
def create_vector_store(request_id, documents):
    vectorstore_faiss=FAISS.from_documents(documents, bedrock_embeddings)
    file_name=f"{request_id}.bin"
    folder_path="/tmp"
    vectorstore_faiss.save_local(index_name=file_name, folder_path=folder_path)
    
    ## upload to s3
    s3_client.upload_file(Filename=folder_path + "/" + file_name + ".faiss", Bucket=BUCKET_NAME, Key="my_faiss.faiss")
    s3_client.upload_file(Filename=folder_path + "/" + file_name + ".pkl", Bucket=BUCKET_NAME, Key="my_faiss.pkl")
    return True

def get_unique_id():
    return str(uuid.uuid4())

folder_path="/tmp/"

## Load index
def load_index():
    s3_client.download_file(Bucket=BUCKET_NAME, Key="my_faiss.faiss", Filename=f"{folder_path}my_faiss.faiss")
    s3_client.download_file(Bucket=BUCKET_NAME, Key="my_faiss.pkl", Filename=f"{folder_path}my_faiss.pkl")

def get_llm():
    llm=Bedrock(model_id="ai21.j2-mid-v1", client=bedrock_client,
                model_kwargs={'maxTokens':512})
    return llm

## get response
def get_response(llm, vectorstore, question ):
    ## create prompt / template
    prompt_template = """

    Human: Please use the given context to provide concise answer to the question
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    <context>
    {context}
    </context>

    Question: {question}

    Assistant:"""

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(
        search_type="similarity", search_kwargs={"k": 5}
    ),
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT}
    )
    answer=qa({"query":question})
    return answer['result']


## Main methode
def main():
    st.header("CHAT WITH PDF")
    uploaded_file = st.file_uploader("Choose a file", "pdf")
    if uploaded_file is not None:
        request_id = get_unique_id()        
        saved_file_name = f"{request_id}.pdf"
        with open(saved_file_name, mode="wb") as w:
            w.write(uploaded_file.getvalue())        
        loader = PyPDFLoader(saved_file_name)
        pages = loader.load_and_split()
        st.write(f"Total Pages: {len(pages)}")

        ## Split Text
        splitted_docs = split_text(pages, 1000, 200)
        result = create_vector_store(request_id, splitted_docs)
        if result is False:            
            st.write("Error!! Please check logs")
        load_index()
        dir_list = os.listdir(folder_path)

        ## create index
        faiss_index = FAISS.load_local(
            index_name="my_faiss",
            folder_path = folder_path,
            embeddings=bedrock_embeddings,
            allow_dangerous_deserialization=True
        )

        st.write("Index Is Ready")
        question = st.text_input("Please ask your question based on the uploaded file")
        if st.button("Ask Question"):
            with st.spinner("Processing..."):

                llm = get_llm()
                st.write(get_response(llm, faiss_index, question))
                st.success("Done")

if __name__ == "__main__":
    main()