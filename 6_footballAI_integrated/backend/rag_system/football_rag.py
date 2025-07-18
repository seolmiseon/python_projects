import streamlit as st
import pandas as pd
import os
from typing import Dict, List, Any
from langchain_upstage import UpstageEmbeddings, ChatUpstage
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.documents import Document
from dotenv import load_dotenv
import uuid
import time

load_dotenv()

# 축구 데이터 샘플 (실제로는 API나 데이터베이스에서 가져올 수 있음)
FOOTBALL_DATA = [
    {
        "content": "손흥민은 2023-24 시즌 프리미어리그에서 17골 9도움을 기록했습니다. 토트넘의 주장으로서 팀을 이끌며 공격의 핵심 역할을 담당하고 있습니다.",
        "metadata": {"player": "손흥민", "team": "토트넘", "position": "공격수", "season": "2023-24"}
    },
    {
        "content": "김민재는 바이에른 뮌헨에서 중앙 수비수로 활약하며 2023-24 시즌 분데스리가에서 27경기에 출전했습니다. 강력한 수비력과 빌드업 능력으로 팀의 핵심 수비수입니다.",
        "metadata": {"player": "김민재", "team": "바이에른 뮌헨", "position": "수비수", "season": "2023-24"}
    },
    {
        "content": "이강인은 파리 생제르맹에서 미드필더로 활약하며 2023-24 시즌 리그앙에서 3골 4도움을 기록했습니다. 창의적인 패스와 드리블 능력이 뛰어납니다.",
        "metadata": {"player": "이강인", "team": "파리 생제르맹", "position": "미드필더", "season": "2023-24"}
    },
    {
        "content": "토트넘은 2023-24 시즌 프리미어리그에서 4위를 기록했습니다. 앙게 포스테코글루 감독의 공격적 축구로 많은 팬들의 사랑을 받고 있습니다.",
        "metadata": {"team": "토트넘", "league": "프리미어리그", "position": "4위", "season": "2023-24"}
    },
    {
        "content": "바이에른 뮌헨은 2023-24 시즌 분데스리가에서 2위를 기록했습니다. 하리 케인과 함께 공격력을 강화했지만 리버풀에게 우승을 내주었습니다.",
        "metadata": {"team": "바이에른 뮌헨", "league": "분데스리가", "position": "2위", "season": "2023-24"}
    }
]

def create_football_vectorstore():
    """축구 데이터로 벡터스토어 생성"""
    documents = [Document(page_content=item["content"], metadata=item["metadata"]) 
                 for item in FOOTBALL_DATA]
    
    vectorstore = Chroma.from_documents(
        documents, 
        UpstageEmbeddings(model="solar-embedding-1-large")
    )
    return vectorstore

def setup_football_rag():
    """축구 RAG 체인 설정"""
    vectorstore = create_football_vectorstore()
    retriever = vectorstore.as_retriever(k=3)
    
    chat = ChatUpstage(upstage_api_key=os.getenv("UPSTAGE_API_KEY"))
    
    # 대화 컨텍스트를 고려한 질문 재구성
    contextualize_q_system_prompt = """이전 대화 내용과 최신 사용자 질문이 있을 때, 축구 관련 질문을 독립적으로 이해할 수 있는 형태로 재구성하세요."""
    
    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    
    history_aware_retriever = create_history_aware_retriever(
        chat, retriever, contextualize_q_prompt
    )
    
    # 축구 전문 답변을 위한 시스템 프롬프트
    qa_system_prompt = """당신은 축구 전문 분석가입니다. 사용자의 축구 관련 질문에 대해 정확하고 유용한 정보를 제공하세요.
    
    답변 형식:
    📍 분석 결과: [주요 내용]
    📍 관련 정보: [추가 정보]
    📍 출처: [참고한 데이터]
    
    {context}"""
    
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    
    question_answer_chain = create_stuff_documents_chain(chat, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    
    return rag_chain

def main():
    st.set_page_config(page_title="⚽ 축구 AI 분석가", layout="wide")
    
    st.title("⚽ 축구 AI 분석가")
    st.markdown("축구 선수, 팀, 경기에 대해 무엇이든 물어보세요!")
    
    # 세션 상태 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "rag_chain" not in st.session_state:
        with st.spinner("축구 데이터를 로딩 중..."):
            st.session_state.rag_chain = setup_football_rag()
        st.success("축구 AI 분석가가 준비되었습니다! 🎉")
    
    # 사이드바에 축구 관련 정보 표시
    with st.sidebar:
        st.header("📊 축구 데이터")
        st.markdown("""
        **현재 포함된 데이터:**
        - 선수 정보 (손흥민, 김민재, 이강인)
        - 팀 정보 (토트넘, 바이에른 뮌헨)
        - 2023-24 시즌 통계
        """)
        
        st.header("💡 질문 예시")
        st.markdown("""
        - "손흥민이 올해 몇 골 넣었어?"
        - "김민재는 어떤 팀에서 뛰고 있어?"
        - "토트넘은 올해 리그에서 몇 위야?"
        - "이강인의 플레이 스타일은?"
        """)
    
    # 채팅 인터페이스
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("축구에 대해 무엇이든 물어보세요!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            try:
                result = st.session_state.rag_chain.invoke({
                    "input": prompt, 
                    "chat_history": st.session_state.messages
                })
                
                # 증거 컨텍스트 표시
                with st.expander("🔍 참고한 정보"):
                    for i, doc in enumerate(result["context"], 1):
                        st.markdown(f"**정보 {i}:** {doc.page_content}")
                        st.caption(f"메타데이터: {doc.metadata}")
                
                # 답변 스트리밍 효과
                full_response = ""
                for chunk in result["answer"].split(" "):
                    full_response += chunk + " "
                    time.sleep(0.1)
                    message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error(f"오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main() 