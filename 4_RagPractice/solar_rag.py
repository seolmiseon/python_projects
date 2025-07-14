# import time
# import os
# import base64
# import uuid
# import tempfile
# from typing import Dict, List, Any, Optional
# from langchain_upstage import UpstageEmbeddings
# from langchain_chroma import Chroma
# from langchain_community.document_loaders import PyPDFLoader

# from langchain_upstage import ChatUpstage
# from langchain_core.messages import HumanMessage, SystemMessage

# from langchain.chains import create_history_aware_retriever
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# from langchain.chains import create_retrieval_chain
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from dotenv import load_dotenv
# import streamlit as st




# if "id" not in st.session_state:
#     st.session_state.id = uuid.uuid4()
#     st.session_state.file_cache = {}
# session_id = st.session_state.id
# client = None
# def reset_chat():
#     st.session_state.messages = []
#     st.session_state.context = None
# def display_pdf(file):
#     st.markdown("### PDF Preview")
#     base64_pdf = base64.b64encode(file.read()).decode("utf-8")
#     pdf_display = f"""<iframe src="data:application/pdf;base64,{base64_pdf}" width="400" height="100%" type="application/pdf" style="height:100vh; width:100%"></iframe>"""
#     st.markdown(pdf_display, unsafe_allow_html=True)
# with st.sidebar:
#     st.header(f"Add your documents!")
#     uploaded_file = st.file_uploader("Choose your `.pdf` file", type="pdf")
# if uploaded_file:
#     print(uploaded_file)
#     try:
#         file_key = f"{session_id}-{uploaded_file.name}"
# with tempfile.TemporaryDirectory() as temp_dir:
#     file_path = os.path.join(temp_dir, uploaded_file.name)
#     print("file path:", file_path)
#     with open(file_path, "wb") as f:
#         f.write(uploaded_file.getvalue())
# file_key = f"{session_id}-{uploaded_file.name}"
# st.write("Indexing your document...")
# if file_key not in st.session_state.get('file_cache', {}):
#     if os.path.exists(temp_dir):
#         print("temp_dir:", temp_dir)
#         loader = PyPDFLoader(file_path)
# else:
#     st.error('Could not find the file you uploaded, please check again...')
#     st.stop()
# pages = loader.load_and_split()
# vectorstore = Chroma.from_documents(pages, UpstageEmbeddings(model="solar-embedding-1-large"))
# retriever = vectorstore.as_retriever(k=2)
# chat = ChatUpstage(upstage_api_key=os.getenv("UPSTAGE_API_KEY"))
# contextualize_q_system_prompt = """이전 대화 내용과 최신 사용자 질문이 있을 때, 이 질문이 이전 대화 내용과 관련이 있을 수 있습니다. 이런 경우, 대화 내용을 알 필요 없이 독립적으로 이해할 수 있는 질문으로 바꾸세요. 질문에 답할 필요는 없고, 필요하다면 그저 다시 구성하거나 그대로 두세요."""

# contextualize_q_prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", contextualize_q_system_prompt),
#         MessagesPlaceholder("chat_history"),
#         ("human", "{input}"),
#     ]
# )
# history_aware_retriever = create_history_aware_retriever(
#     chat, retriever, contextualize_q_prompt
# )
# qa_system_prompt = """질문-답변 업무를 돕는 보조원입니다. 질문에 답하기 위해 검색된 내용을 사용하세요. 답을 모르면 모른다고 말하세요. 답변은 세 문장 이내로 간결하게 유지하세요.
# ## 답변 예시
# 📍답변 내용:
# 📍증거:
# {context}"""
# qa_prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", qa_system_prompt),
#         MessagesPlaceholder("chat_history"),
#         ("human", "{input}"),
#     ]
# )
# question_answer_chain = create_stuff_documents_chain(chat, qa_prompt)
# rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
# st.success("Ready to Chat!")
# display_pdf(uploaded_file)
# st.title("Solar LLM Chatbot")
# if "openai_model" not in st.session_state:
#     st.session_state["openai_model"] = "gpt-3.5-turbo"
# if "messages" not in st.session_state:
#     st.session_state.messages = []
# MAX_MESSAGES_BEFORE_DELETION = 4


# if prompt := st.chat_input("Ask a question!"):
#     if len(st.session_state.messages) >= MAX_MESSAGES_BEFORE_DELETION:
#         del st.session_state.messages[0]
#         del st.session_state.messages[0]
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)

# with st.chat_message("assistant"):
#     message_placeholder = st.empty()
#     full_response = ""
#     result = rag_chain.invoke({"input": prompt, "chat_history": st.session_state.messages})
#     with st.expander("Evidence context"):
#         st.write(result["context"])
#     for chunk in result["answer"].split(" "):
#         full_response += chunk + " "
#         time.sleep(0.2)
#         message_placeholder
 
# response = chat.invoke(messages)
# print(response)