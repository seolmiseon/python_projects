import streamlit as st
import tempfile
import os
import base64
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_upstage import UpstageEmbeddings
from config import config

def upload_and_process_pdf(uploaded_file):
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())
            
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()
        embeddings = UpstageEmbeddings(
            model="solar-embedding-1-large",
            upstage_api_key=config.UPSTAGE_API_KEY
        )
        vectorstore = Chroma.from_documents(pages, embeddings)
        retriever = vectorstore.as_retriever(k=2)
        
        display_pdf(uploaded_file)
        return vectorstore, retriever
    
def display_pdf(file):
    st.markdown("### PDF Preview")
    base64_pdf = base64.b64encode(file.getvalue()).decode("utf-8")
    pdf_display = f"""<iframe src='data:application/pdf;base64,{base64_pdf}' width='100%' height='600px'></iframe>"""
    st.markdown(pdf_display, unsafe_allow_html=True)    