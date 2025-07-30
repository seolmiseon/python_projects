import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
# from langchain_community.chat_models import ChatOpenAI  # 사용하지 않으므로 주석 처리
from langchain_upstage import ChatUpstage
from transformers import pipeline
import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# OpenAI 관련 환경변수 강제 제거
if 'OPENAI_API_KEY' in os.environ:
    del os.environ['OPENAI_API_KEY']
if 'OPENAI_API_BASE' in os.environ:
    del os.environ['OPENAI_API_BASE']

# Streamlit Cloud 환경변수 설정 (배포 시 사용)
if 'UPSTAGE_API_KEY' not in os.environ:
    os.environ['UPSTAGE_API_KEY'] = st.secrets.get('UPSTAGE_API_KEY', '')
if 'HUGGINGFACEHUB_API_TOKEN' not in os.environ:
    os.environ['HUGGINGFACEHUB_API_TOKEN'] = st.secrets.get('HUGGINGFACEHUB_API_TOKEN', '')

# 페이지 설정
st.set_page_config(
    page_title="기본 대화 기억 챗봇",
    layout="wide"
)

# 제목
st.title("기본 대화 기억 챗봇")
st.markdown("---")

# 사이드바 - 설정
with st.sidebar:
    st.header("설정")
    
    # Upstage API 키 입력 (Streamlit Secrets 우선, 환경변수 차선)
    upstage_key = st.text_input(
        "Upstage API 키",
        type="password",
        value=st.secrets.get("UPSTAGE_API_KEY", "") or os.getenv("UPSTAGE_API_KEY", ""),
        help="Upstage에서 발급받은 API 키를 입력하세요"
    )
    
    # Hugging Face API 토큰 입력
    hf_token = st.text_input(
        "Hugging Face API 토큰",
        type="password",
        value=st.secrets.get("HUGGINGFACEHUB_API_TOKEN", "") or os.getenv("HUGGINGFACEHUB_API_TOKEN", ""),
        help="Hugging Face에서 발급받은 API 토큰을 입력하세요"
    )
    
    if upstage_key:
        os.environ["UPSTAGE_API_KEY"] = upstage_key
        st.success("Upstage API 키가 설정되었습니다!")
    
    if hf_token:
        os.environ["HUGGINGFACEHUB_API_TOKEN"] = hf_token
        st.success("Hugging Face API 토큰이 설정되었습니다!")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation" not in st.session_state:
    st.session_state.conversation = None

if "sentiment_analyzer" not in st.session_state:
    st.session_state.sentiment_analyzer = None

# 감정 분석 파이프라인 초기화
@st.cache_resource
def load_sentiment_analyzer():
    """Hugging Face 파이프라인을 사용한 감정 분석"""
    try:
        # 가벼운 영어 감정 분석 모델 사용
        analyzer = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest",
            return_all_scores=False
        )
        return analyzer
    except Exception as e:
        st.error(f"감정 분석 모델 로드 실패: {e}")
        return None

# LangChain 대화 체인 초기화
def initialize_conversation(api_key):
    """대화 체인 초기화"""
    try:
        # 메모리 설정 (대화 기억)
        memory = ConversationBufferMemory()
        
        # LLM 설정 (Upstage Solar 모델 사용)
        llm = ChatUpstage(
            model="solar-1-mini-chat",
            temperature=0.7,
            api_key=api_key
        )
        
        # 대화 체인 생성
        conversation = ConversationChain(
            llm=llm,
            memory=memory,
            verbose=True
        )
        
        return conversation
    except Exception as e:
        st.error(f"대화 체인 초기화 실패: {e}")
        return None

# 감정 분석 함수
def analyze_sentiment(text):
    """텍스트의 감정 분석"""
    if st.session_state.sentiment_analyzer is None:
        return "분석 불가"
    
    try:
        result = st.session_state.sentiment_analyzer(text)
        # Hugging Face 파이프라인 결과 처리
        if result and len(result) > 0:
            sentiment = result[0]
            return f"{sentiment['label']} ({sentiment['score']:.2f})"
        return "분석 실패"
    except Exception as e:
        return f"오류: {e}"

# 메인 앱
def main():
    # 감정 분석 모델 로드
    if st.session_state.sentiment_analyzer is None:
        st.session_state.sentiment_analyzer = load_sentiment_analyzer()
    
    # 대화 체인 초기화
    if st.session_state.conversation is None and upstage_key:
        with st.spinner("대화 체인을 초기화하는 중..."):
            st.session_state.conversation = initialize_conversation(upstage_key)
    
    # 채팅 인터페이스
    st.subheader("대화하기")
    
    # 이전 메시지들 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # 챗봇 응답에 감정 분석 결과 표시
            if message["role"] == "assistant" and "sentiment" in message:
                st.info(f"감정 분석: {message['sentiment']}")
    
    # 사용자 입력
    if prompt := st.chat_input("메시지를 입력하세요..."):
        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # 챗봇 응답 생성
        if st.session_state.conversation:
            with st.chat_message("assistant"):
                with st.spinner("생각하는 중..."):
                    response = st.session_state.conversation.predict(input=prompt)
                    st.markdown(response)
                
                # 감정 분석
                sentiment = analyze_sentiment(response)
                st.info(f"감정 분석: {sentiment}")
                
                # 응답 저장
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response,
                    "sentiment": sentiment
                })
        else:
            st.error("대화 체인이 초기화되지 않았습니다. Upstage API 키를 확인해주세요.")
    
    # 대화 기록 초기화 버튼
    if st.button("대화 기록 초기화"):
        st.session_state.messages = []
        st.session_state.conversation = None
        # API 키가 있으면 대화 체인 재초기화
        if upstage_key:
            with st.spinner("대화 체인을 재초기화하는 중..."):
                st.session_state.conversation = initialize_conversation(upstage_key)
        st.rerun()

if __name__ == "__main__":
    main() 