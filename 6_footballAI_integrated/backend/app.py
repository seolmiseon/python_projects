import streamlit as st
from rag_chain import setup_rag_chain
from chat_interface import handle_user_input, display_chat_history
from config import initialize_session_state, config
from dotenv import load_dotenv

load_dotenv()

def main():
    initialize_session_state()
    
    st.title("Solar LLM chatbot")
    
    with st.sidebar:
        st.header("Add your documents!")

        st.subheader("Chunk Size")
        chunk_size_option = st.selectbox(
            "Chunk Size",
            options=list(config.CHUNK_SIZE_OPTIONS.keys()),
            index=1,
            help="Small: 대화형 문서, Medium: 일반 문서, Large: 기술 문서, XLarge: 긴 논문"
        )
        uploaded_file = st.file_uploader("Choose your `.pdf` file", type="pdf")
    
    if uploaded_file:
        config.set_chunk_size(chunk_size_option)
        vectorstore, retriever = upload_and_process_pdf(uploaded_file,config.CHUNK_SIZE)
        rag_chain = setup_rag_chain(retriever)
        
        st.success("Ready to Chat!")
        display_chat_history()
        
        if prompt := st.chat_input("Ask a question!"):
            handle_user_input(prompt, rag_chain)
            
if __name__ == "__main__":
    main()