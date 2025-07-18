import streamlit as st
import time


def handle_user_input(prompt, rag_chain):
    st.session_state.messages.append({"role": "user", "content" : prompt})
    with st.chat_message("user"):
        st.write(prompt)
        
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        result = rag_chain.invoke({"input": prompt, "chat_history": st.session_state.messages})
        with st.expander("Evidence context"):
            st.write(result["context"])
        for chunk in result["answer"].split(" "):
            full_response += chunk + " "
            message_placeholder.write(chunk + " ")
            time.sleep(0.3)
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content" : full_response})
    
    
def display_chat_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])