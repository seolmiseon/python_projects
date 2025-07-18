import streamlit as st
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY")
    CHUNK_SIZE_OPTIONS = {
    "Small": 1000,
    "Medium": 2000,
    "Large": 3000,
    "XLarge": 4000
}
    CHUNK_SIZE = CHUNK_SIZE_OPTIONS["Medium"]
    CHUNK_OVERLAP = 200

    if not UPSTAGE_API_KEY:
        raise ValueError("UPSTAGE_API_KEY not found in environment variables")

    @classmethod
    def set_chunk_size(cls,size_name):
        if size_name in cls.CHUNK_SIZE_OPTIONS:
            cls.CHUNK_SIZE = cls.CHUNK_SIZE_OPTIONS[size_name]
        else:
           raise ValueError(f"Invalid chunk size: {size_name}. Available options are: {list(cls.CHUNK_SIZE_OPTIONS.keys())}")

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