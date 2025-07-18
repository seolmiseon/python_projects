import os
from langchain_upstage import ChatUpstage
from langchain_core.utils import get_from_env
from dotenv import load_dotenv

load_dotenv()

UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY")
if not UPSTAGE_API_KEY:
    raise ValueError("UPSTAGE_API_KEY not found in environment variables")

def classify_bus_info_with_solar_mini(bus_data):
    """
    solar-mini를 사용하여 버스 정보를 분류하는 함수
    - 정류장 유형, 혼잡도, 시간대 등을 분류
    """
    chat = ChatUpstage(
        api_key=UPSTAGE_API_KEY,  # type: ignore
        model="solar-mini"
    )
    
    prompt = f"""
    다음 버스 정보를 분석하여 분류해주세요:
    
    버스 정보: {bus_data}
    
    다음 카테고리로 분류해주세요:
    1. 정류장 유형 (시내버스/시외버스/마을버스)
    2. 시간대 (출근시간/퇴근시간/일반시간)
    3. 혼잡도 (혼잡/보통/여유)
    4. 특별상황 (첫차/막차/배차간격 긴 시간대)
    
    JSON 형태로 응답해주세요.
    """
    
    try:
        response = chat.invoke(prompt)
        if hasattr(response, 'content'):
            content = response.content
            if isinstance(content, str):
                return content
            elif isinstance(content, list):
                return str(content[0]) if content else ""
            else:
                return str(content)
        elif isinstance(response, str):
            return response
        else:
            return str(response)
    except Exception as e:
        print(f"Solar-mini 분류 오류: {e}")
        return None

def generate_final_notice_with_solar_pro(classified_info, bus_number):
    """
    solar-pro를 사용하여 최종 안내문구를 생성하는 함수
    - 분류된 정보를 바탕으로 개인화된 안내문구 생성
    """
    chat = ChatUpstage(
        api_key=UPSTAGE_API_KEY,  # type: ignore
        model="solar-pro"
    )
    
    prompt = f"""
    다음 정보를 바탕으로 시각장애인을 위한 친절한 버스 안내문구를 생성해주세요:
    
    버스 번호: {bus_number}
    분류 정보: {classified_info}
    
    요구사항:
    1. 시각장애인이 쉽게 이해할 수 있는 명확한 표현
    2. 상황에 맞는 추가 정보 제공 (혼잡도, 배차간격 등)
    3. 친근하고 안전한 톤
    4. 50자 이내로 간결하게
    
    안내문구만 출력해주세요.
    """
    
    try:
        response = chat.invoke(prompt)
        if hasattr(response, 'content'):
            content = response.content
            if isinstance(content, str):
                return content.strip()
            elif isinstance(content, list):
                return str(content[0]).strip() if content else f"이 버스는 {bus_number}번 버스입니다."
            else:
                return str(content).strip()
        elif isinstance(response, str):
            return response.strip()
        else:
            return str(response).strip()
    except Exception as e:
        print(f"Solar-pro 생성 오류: {e}")
        return f"이 버스는 {bus_number}번 버스입니다."

def get_bus_context_info(bus_number, city_code):
    """
    버스 번호와 도시코드로 기본 컨텍스트 정보 생성
    """
    return {
        "bus_number": bus_number,
        "city_code": city_code,
        "timestamp": "현재시간",
        "route_type": "시내버스" if city_code in ["11", "25"] else "시외버스"
    }
