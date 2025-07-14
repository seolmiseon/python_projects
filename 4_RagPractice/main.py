import streamlit as st
from rag_chain import setup_rag_chain
from chat_interface import handle_user_input, display_chat_history
from pdf_utils import upload_and_process_pdf
from config import initialize_session_state


def main():
    initialize_session_state()
    
    st.title("Solar LLM chatbot")
    
    with st.sidebar:
        st.header("Add your documents!")
        uploaded_file = st.file_uploader("Choose your `.pdf` file", type="pdf")
    
    if uploaded_file:
        vectorstore, retriever = upload_and_process_pdf(uploaded_file)
        rag_chain = setup_rag_chain(retriever)
        
        st.success("Ready to Chat!")
        display_chat_history()
        
        if prompt := st.chat_input("Ask a question!"):
            handle_user_input(prompt, rag_chain)
            
if __name__ == "__main__":
    main()