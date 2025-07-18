import os
from dotenv import load_dotenv

load_dotenv()

# langchain_upstage 패키지 import 시도
try:
    from langchain_upstage import ChatUpstage
    UPSTAGE_AVAILABLE = True
except ImportError:
    UPSTAGE_AVAILABLE = False
    print("langchain_upstage 패키지를 찾을 수 없습니다. 더미 모드로 실행됩니다.")

UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY")

def classify_bus_info_with_solar_mini(context_info):
    """Solar-mini로 버스 정보 분류"""
    if not UPSTAGE_API_KEY or not UPSTAGE_AVAILABLE:
        # API 키가 없거나 패키지가 없으면 더미 데이터 반환
        return {
            "bus_type": "일반 시내버스",
            "route_type": "도시형", 
            "service_class": "일반"
        }
    
    try:
        llm = ChatUpstage(
            upstage_api_key=UPSTAGE_API_KEY,
            model="solar-1-mini-chat"
        )
        
        prompt = f"""
        다음 버스 정보를 분석해서 분류해주세요:
        {context_info}
        
        다음 형식으로 답변해주세요:
        - 버스 타입: (일반 시내버스/광역버스/마을버스/공항버스 등)
        - 노선 유형: (도시형/좌석형/직행형 등)
        - 서비스 등급: (일반/급행/직행 등)
        """
        
        response = llm.invoke(prompt)
        return {
            "bus_type": "일반 시내버스",
            "route_type": "도시형",
            "service_class": "일반",
            "raw_response": response.content
        }
    except Exception as e:
        # 에러 발생시 더미 데이터 반환
        return {
            "bus_type": "일반 시내버스",
            "route_type": "도시형",
            "service_class": "일반",
            "error": str(e)
        }

def classify_bus_info_with_solar_mini(context_info):
    """Solar-mini로 버스 정보 분류 (더미 함수)"""
    # API 키가 없으면 더미 데이터 반환
    if UPSTAGE_API_KEY == "dummy_key":
        return {
            "bus_type": "일반 시내버스",
            "route_type": "도시형",
            "service_class": "일반"
        }
    
    # 실제 API 호출은 여기에 구현
    return None

def generate_final_notice_with_solar_pro(classified_info, bus_number):
    """
    solar-pro를 사용하여 최종 안내문구를 생성하는 함수 (더미 함수)
    - 분류된 정보를 바탕으로 개인화된 안내문구 생성
    """
    # API 키가 없으면 더미 데이터 반환
    if UPSTAGE_API_KEY == "dummy_key":
        return f"이 버스는 {bus_number}번 버스입니다. 안전한 탑승 바랍니다."
    
    # 실제 API 호출은 여기에 구현
    return f"이 버스는 {bus_number}번 버스입니다."
    
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