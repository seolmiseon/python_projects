import streamlit as st
from bus_api import get_route_info
from llm_prompt import generate_notice_word
from solar_api import classify_bus_info_with_solar_mini, generate_final_notice_with_solar_pro, get_bus_context_info
from rag_system import rag_system
import requests
import base64
from dotenv import load_dotenv
import os
import json
import time

load_dotenv()
GOOGLE_TTS_API_KEY = os.getenv("GOOGLE_TTS_API_KEY")


def google_tts(text, filename="output.mp3"):
    url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={GOOGLE_TTS_API_KEY}"
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data = {
        "input": {"text": text},
        "voice": {"languageCode": "ko-KR", "name": "ko-KR-Wavenet-A"},
        "audioConfig": {"audioEncoding": "MP3"}
    }
    response = requests.post(url, headers=headers, json=data)
    audio_content = response.json()["audioContent"]
    with open(filename, "wb") as out:
        out.write(base64.b64decode(audio_content))
    return filename



def enhanced_bus_notice_system():
    """향상된 버스 안내 시스템 (Solar API + RAG)"""
    st.subheader("🚌 향상된 버스 안내 시스템")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 사용자 친화적 도시 선택
        city_options = {
            "대전": "25",
            "서울": "11", 
            "부산": "21",
            "광주": "12"
        }
        selected_city = st.selectbox("도시 선택", list(city_options.keys()), key="enhanced_city")
        city_code = city_options[selected_city]
        
        bus_number_input = st.text_input("버스 번호 입력", value="108", help="예: 108번", key="enhanced_bus")
    
    with col2:
        use_solar_api = st.checkbox("Solar API 사용", value=True)
        use_rag = st.checkbox("RAG 시스템 사용", value=True)
    
    # 기본 노선ID 매핑
    route_mapping = {
        ("25", "108"): "DJB30300004",  # 대전 108번
        ("11", "146"): "100100118",    # 서울 146번  
        ("21", "57"): "5200057000",    # 부산 57번
    }
    
    if st.button("향상된 안내문구 생성"):
        route_id = route_mapping.get((city_code, bus_number_input), "DJB30300004")  # 기본값
        
        if city_code and route_id:
            with st.spinner("버스 정보를 분석 중..."):
                # 1. 기본 버스 정보 가져오기 (임시: 사용자 입력값 사용)
                bus_number = bus_number_input
                
                if bus_number:
                    # 2. 컨텍스트 정보 생성
                    context_info = get_bus_context_info(bus_number, city_code)
                    
                    # 3. Solar-mini로 분류 (작은 모델)
                    if use_solar_api:
                        st.info("Solar-mini로 버스 정보 분류 중...")
                        classified_info = classify_bus_info_with_solar_mini(context_info)
                        if classified_info:
                            st.json(classified_info)
                        else:
                            classified_info = "일반적인 시내버스 정보"
                    else:
                        classified_info = "일반적인 시내버스 정보"
                    
                    # 4. RAG로 관련 정보 검색
                    if use_rag:
                        st.info("🔍 RAG로 관련 정보 검색 중...")
                        rag_results = rag_system.search_bus_info(f"{bus_number}번 버스 정보")
                        if rag_results:
                            with st.expander("RAG 검색 결과"):
                                for i, doc in enumerate(rag_results, 1):
                                    st.markdown(f"**결과 {i}:** {doc.page_content}")
                                    st.caption(f"메타데이터: {doc.metadata}")
                    
                    # 5. Solar-pro로 최종 안내문구 생성 (큰 모델)
                    if use_solar_api:
                        st.info("Solar-pro로 최종 안내문구 생성 중...")
                        final_notice = generate_final_notice_with_solar_pro(classified_info, bus_number)
                    else:
                        final_notice = f"이 버스는 {bus_number}번 버스입니다."
                    
                    # 6. 결과 표시
                    st.success("✅ 안내문구 생성 완료!")
                    st.markdown(f"**생성된 안내문구:** {final_notice}")
                    
                    # 7. TTS 변환 및 재생
                    st.info("🎵 음성 변환 중...")
                    # 동적 파일명 생성으로 TTS 캐시 문제 해결
                    filename = f"output_{int(time.time())}.mp3"
                    google_tts(final_notice, filename)
                    st.audio(filename)
                    
                    # 8. 기존 방식과 비교
                    with st.expander("기존 방식과 비교"):
                        old_notice = generate_notice_word(bus_number)
                        st.markdown(f"**기존 방식:** {old_notice}")
                        st.markdown(f"**향상된 방식:** {final_notice}")
                        
                else:
                    st.warning("버스 정보를 불러오지 못했습니다.")
        else:
            st.warning("도시와 버스 번호를 입력해주세요")

def main():
    st.title('🚌 버스별 음성 안내 시스템 (Solar API + RAG)')
    
    # 사이드바에 기능 선택
    st.sidebar.title("기능 선택")
    mode = st.sidebar.selectbox(
        "모드를 선택하세요",
        ["기본 안내 시스템", "향상된 안내 시스템"]
    )
    
    if mode == "기본 안내 시스템":
        st.subheader("🔧 기본 안내 시스템")
        
        # 사용자 친화적 입력 방식
        col1, col2 = st.columns(2)
        with col1:
            city_options = {
                "대전": "25",
                "서울": "11", 
                "부산": "21",
                "광주": "12"
            }
            selected_city = st.selectbox("도시 선택", list(city_options.keys()))
            city_code = city_options[selected_city]
        
        with col2:
            bus_number_input = st.text_input("버스 번호 입력", value="108", help="예: 108번")
        
        # 기본 노선ID 매핑 (시연용)
        route_mapping = {
            ("25", "108"): "DJB30300004",  # 대전 108번
            ("11", "146"): "100100118",    # 서울 146번  
            ("21", "57"): "5200057000",    # 부산 57번
        }
        
        if st.button("안내문구 생성"):
            route_id = route_mapping.get((city_code, bus_number_input), "DJB30300004")  # 기본값
            
            if city_code and route_id:
                # 임시: API 대신 사용자 입력값 사용
                bus_number = bus_number_input
                if bus_number:
                    notice = f"이 버스는 {bus_number}번 버스입니다."
                    st.success(f"안내문구: {notice}")
                    print("TTS로 넘길 notice:", notice, type(notice))
                    
                    # 동적 파일명 생성으로 TTS 캐시 문제 해결
                    filename = f"output_{int(time.time())}.mp3"
                    google_tts(notice, filename)
                    st.audio(filename)
                else:
                   st.warning("버스 정보를 불러오지 못했습니다.")
            else:
                st.warning("도시코드와 노선ID를 입력해주세요")
    
    elif mode == "향상된 안내 시스템":
        enhanced_bus_notice_system()
    
  
    
    # 사이드바에 정보 표시
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 시스템 정보")
    st.sidebar.markdown("""
    **Solar API 사용:**
    - solar-mini: 버스 정보 분류
    - solar-pro: 안내문구 생성
    
    **RAG 시스템:**
    - ChromaDB 벡터스토어
    - 청크 크기 최적화
    - 버스 관련 문서 검색
    """)

if __name__ == "__main__":
    main() 