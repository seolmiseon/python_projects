import streamlit as st
from bus_api import get_route_info
from llm_prompt import generate_notice_word
import requests
import base64
from dotenv import load_dotenv
import os

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
    
def main():
    st.title('버스별 음성 안내 시스템')
    city_code = st.text_input("도시코드 입력", value="25", help="예: 25(대전), 11(서울)")
    route_id = st.text_input("노선 ID 입력", value="DJB30300004", help="예: DJB30300004")
    if st.button("안내문구 생성"):
        if city_code and route_id:
            bus_number = get_route_info(city_code, route_id)
            if bus_number:
                notice = f"이 버스는 {bus_number}번 버스입니다."
                st.success(f"안내문구: {notice}")
                print("TTS로 넘길 notice:", notice, type(notice))
                text_to_speech(notice)
                st.audio("output.wav")
            else:
               st.warning("버스 정보를 불러오지 못했습니다.")
        else:
            st.warning("도시코드드,노선ID를 입력해주세요")        

if __name__ == "__main__":
    main() 