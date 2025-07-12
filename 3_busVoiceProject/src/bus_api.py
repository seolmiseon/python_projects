import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_route_info(city_code, route_id):
    api_key = os.getenv("PUBLIC_DATA_API_KEY")
    url = "http://apis.data.go.kr/1613000/BusRouteInfoInqireService/getRouteInfoIem"
    params = {
        "serviceKey": api_key,
        "cityCode": city_code,
        "routeId": route_id,
        "_type": "json"
    }
    
    print("API 요청 URL:", url)
    print("API 요청 파라미터:", params)

    response = requests.get(url, params=params)
    print("응답 상태코드:", response.status_code)

    if response.status_code == 200:
        data = response.json()
        print("전체 API 응답:", data) 

        try:
            items = data["response"]["body"]["items"]
            print("items 타입:", type(items))
            print("items 내용:", items)
            
           # items가 빈 문자열인지 확인
            if not items or items == "":
                print("items가 비어있음")
                return None
            
            # items가 'item' 키를 가진 딕셔너리인 경우
            if isinstance(items, dict) and "item" in items:
                item = items["item"]
                if "routeno" in item:
                    bus_number = item["routeno"]
                    print("찾은 노선번호:", bus_number)
                    return bus_number
                else:
                    print("routeno 키가 없습니다. 사용 가능한 키:", list(item.keys()))
                    return None
            else:
                print("items가 예상과 다름:", items)
                return None
                
        except KeyError as e:
            print("키 오류:", e)
            print("data 구조:", data)
            return None
    
    else:
        print("API 요청 실패:", response.status_code)
        return None
    
    