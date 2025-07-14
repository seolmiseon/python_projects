import streamlit as st
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY")
    if not UPSTAGE_API_KEY:
        raise ValueError("UPSTAGE_API_KEY not found in environment variables")

config = Config()

def initialize_session_state():
    if "id" not in st.session_state:
        st.session_state.id = uuid.uuid4()
    if "file_cache" not in st.session_state:
        st.session_state.file_cache = {}
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-3.5-turbo"
    if "solar_model" not in st.session_state:
        st.session_state.solar_model = "solar-pro"  
        
def setup_config():
    initialize_session_state()
    return config