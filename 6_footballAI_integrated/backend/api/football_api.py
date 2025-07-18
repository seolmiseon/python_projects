"""
축구 API 통합 모듈
Football API, ScoreBat API, SportDB API를 통합하여 축구 데이터를 제공
"""

import requests
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import json

class FootballAPIClient:
    """축구 API 클라이언트"""
    
    def __init__(self):
        self.football_api_key = os.getenv('FOOTBALL_API_KEY')
        self.scorebat_api_key = os.getenv('SCOREBAT_API_KEY')
        self.base_urls = {
            'football_api': 'https://api.football-api.com/v3',
            'scorebat': 'https://www.scorebat.com/video-api/v3',
            'sportdb': 'https://www.thesportsdb.com/api/v1/json'
        }
    
    def get_date_range(self, days_ago: int = 3, days_future: int = 7) -> tuple:
        """날짜 범위 계산"""
        today = datetime.now()
        past_date = today - timedelta(days=days_ago)
        future_date = today + timedelta(days=days_future)
        
        return (
            past_date.strftime('%Y-%m-%d'),
            future_date.strftime('%Y-%m-%d')
        )
    
    def get_matches(self, league_id: Optional[int] = None) -> Dict[str, Any]:
        """경기 정보 조회"""
        try:
            from_date, to_date = self.get_date_range()
            
            if not self.football_api_key:
                return {"error": "Football API key not found"}
            
            # Football API 호출
            url = f"{self.base_urls['football_api']}/fixtures"
            params = {
                'api_token': self.football_api_key,
                'from': from_date,
                'to': to_date
            }
            
            if league_id:
                params['league_id'] = league_id
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"API Error: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Exception: {str(e)}"}
    
    def get_scorebat_highlights(self) -> Dict[str, Any]:
        """ScoreBat 하이라이트 영상 조회"""
        try:
            if not self.scorebat_api_key:
                return {"error": "ScoreBat API key not found"}
            
            url = f"{self.base_urls['scorebat']}/feed/"
            params = {'token': self.scorebat_api_key}
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"ScoreBat API Error: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Exception: {str(e)}"}
    
    def get_team_info(self, team_name: str) -> Dict[str, Any]:
        """팀 정보 조회 (SportDB API)"""
        try:
            url = f"{self.base_urls['sportdb']}/1/searchteams.php"
            params = {'t': team_name}
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"SportDB API Error: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Exception: {str(e)}"}
    
    def get_player_info(self, player_name: str) -> Dict[str, Any]:
        """선수 정보 조회 (SportDB API)"""
        try:
            url = f"{self.base_urls['sportdb']}/1/searchplayers.php"
            params = {'p': player_name}
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"SportDB API Error: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Exception: {str(e)}"}
    
    def get_league_standings(self, league_id: str) -> Dict[str, Any]:
        """리그 순위표 조회 (SportDB API)"""
        try:
            url = f"{self.base_urls['sportdb']}/1/lookuptable.php"
            params = {'l': league_id, 's': '2024-2025'}
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"SportDB API Error: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Exception: {str(e)}"}

# 사용 예시
if __name__ == "__main__":
    # 환경변수 설정 예시
    # os.environ['FOOTBALL_API_KEY'] = 'your_key_here'
    # os.environ['SCOREBAT_API_KEY'] = 'your_key_here'
    
    client = FootballAPIClient()
    
    # 테스트
    print("축구 API 클라이언트 테스트")
    print("=" * 40)
    
    # 경기 정보 조회 테스트
    matches = client.get_matches()
    print(f"경기 정보: {matches}")
    
    # 팀 정보 조회 테스트
    team_info = client.get_team_info("Manchester United")
    print(f"팀 정보: {team_info}")
