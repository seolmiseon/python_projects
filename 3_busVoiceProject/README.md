# 🚌 Enhanced Bus Voice System

Solar LLM과 RAG 시스템을 활용한 지능형 버스 알림 서비스

## 📋 프로젝트 개요

이 프로젝트는 **버스 승하차 시 자동 음성 안내**를 위한 시스템입니다. 버스 노선 정보를 받아 간단명료한 안내 음성을 생성하고, 시각장애인을 포함한 모든 승객이 쉽게 이해할 수 있도록 TTS(Text-to-Speech)로 변환합니다.

**핵심 목적:** 승하차 시점에 "○○번 버스입니다" 자동 음성 안내

## 🎯 주요 기능

-   **자동 음성 안내**: "○○번 버스입니다" 승하차 시점 음성 출력
-   **간단 버스 조회**: 번호로 버스 노선 정보 확인
-   **TTS 음성 변환**: Google TTS API를 통한 한국어 음성 생성
-   **웹 인터페이스**: Streamlit 기반 간단한 조작 환경

### 고급 기능 (선택적)

-   **AI 자연어 처리**: Solar LLM을 통한 대화형 응답
-   **상황별 맞춤 안내**: RAG 시스템 활용한 상황에 맞는 안내

## 🛠️ 기술 스택

### 핵심 기술

-   **Python 3.11**: 메인 개발 언어
-   **Google TTS API**: 음성 변환 (gTTS)
-   **Streamlit**: 웹 인터페이스
-   **버스 도착정보 API**: 실시간 교통 데이터

### 고급 기능 (선택적)

-   **Solar LLM**: 자연어 처리 및 응답 생성
-   **RAG System**: 상황별 맞춤 응답 생성
-   **ChromaDB**: 벡터 데이터베이스

### 주요 라이브러리

#### AI/ML 관련

-   `langchain==0.3.26` - LLM 체인 구성 프레임워크
-   `langchain-upstage==0.6.0` - Solar LLM 연동
-   `langchain-chroma==0.2.0` - ChromaDB 벡터스토어 연동
-   `chromadb==1.0.13` - 벡터 데이터베이스
-   `transformers==4.53.0` - Hugging Face 트랜스포머
-   `sentence-transformers==4.1.0` - 문장 임베딩
-   `torch==2.7.1` - PyTorch 딥러닝 프레임워크

#### 웹 & 인터페이스

-   `streamlit==1.46.1` - 웹 애플리케이션 프레임워크
-   `requests==2.32.4` - HTTP 요청 라이브러리

#### 데이터 처리

-   `pandas==2.3.0` - 데이터 분석 및 처리
-   `numpy==2.3.1` - 수치 연산
-   `pypdf==5.6.1` - PDF 문서 처리

#### 환경 관리

-   `python-dotenv==1.1.1` - 환경변수 관리
-   `pydantic==2.11.7` - 데이터 검증

#### 기타 유틸리티

-   `tenacity==9.1.2` - 재시도 로직
-   `tqdm==4.67.1` - 진행률 표시
-   `rich==14.0.0` - 터미널 출력 포맷팅

## 📁 프로젝트 구조

```
3_busVoiceProject/
├── src/
│   ├── app.py              # 메인 애플리케이션
│   ├── bus_api.py          # 버스 API 관리
│   ├── solar_api.py        # Solar LLM API
│   ├── rag_system.py       # RAG 검색 시스템
│   ├── llm_prompt.py       # LLM 프롬프트 관리
│   └── output.mp3          # 생성된 음성 파일
├── data/                   # 데이터 파일들
├── docs/                   # 문서
├── requirements.txt        # 의존성 패키지
└── README.md              # 프로젝트 문서
```

## 🚀 설치 및 실행

### 1. 환경 설정

```bash
# 현재 프로젝트는 python_sesac 환경을 사용합니다
pyenv activate python_sesac

# 또는 새로운 가상환경을 만들고 싶다면:
python -m venv bus_env
source bus_env/bin/activate  # Linux/WSL2

# 의존성 설치 (필수)
pip install -r requirements.txt
```

**주요 필수 패키지:**

-   `streamlit` - 웹 인터페이스
-   `requests` - API 통신
-   `python-dotenv` - 환경변수 관리

**AI 기능 사용 시 추가 패키지:**

-   `langchain-upstage` - Solar LLM
-   `chromadb` - 벡터 데이터베이스
-   `transformers` - NLP 모델

### 2. 환경변수 설정

`.env` 파일을 생성하고 필요한 API 키를 설정:

```env
UPSTAGE_API_KEY=your_upstage_api_key_here
GOOGLE_API_KEY=your_api_key_here
```

### 3. 실행

```bash
streamlit run src/app.py
```

브라우저에서 `http://localhost:8501`로 접속하여 웹 인터페이스를 사용할 수 있습니다.

## 💡 사용 예시

### 기본 버스 음성 안내

1. **버스 번호 입력**: "10번" 또는 "10"
2. **자동 음성 생성**: "10번 버스입니다"
3. **TTS 재생**: 음성으로 안내 출력

### 고급 AI 기능 (선택적)

-   **자연어 입력**: "다음 버스 언제 와요?"
-   **상황별 응답**: "10번 버스가 3분 후에 도착합니다"
-   **맞춤형 안내**: 시간대별, 상황별 안내 메시지

## 🔧 주요 모듈 설명

### `enhanced_bus_notice_system()`

-   Solar-mini로 질문 분류 (버스*도착*시간 vs 기타)
-   RAG 시스템으로 관련 정보 검색
-   Solar-pro로 자연스러운 응답 생성
-   Google TTS API로 음성 변환

### RAG System

-   버스 정보 임베딩 및 벡터 검색
-   컨텍스트 기반 정보 검색
-   유사도 기반 관련 정보 추출

### Hugging Face Integration

-   프롬프트 템플릿 관리
-   모델 파이프라인 구성
-   텍스트 전처리 및 후처리

### TTS System

-   Google Text-to-Speech API 연동
-   다양한 음성 옵션 지원
-   MP3 파일 생성 및 재생

## 📈 개발 과정

1. **공공 버스 API 연동**
2. **Solar LLM 통합**
3. **RAG 시스템 구축**
4. **TTS 음성 변환 추가**
5. **전체 시스템 통합 및 최적화**

## 📄 라이선스

This project is part of the SeSAC 허깅페이스활용 LLM AI course learning materials.

## 👨‍💻 개발자

-   개발자: seolmiseon
-   과정: SeSAC AI 교육과정
-   날짜: 2024.07.16

---

**Note**: 이 프로젝트는 학습 목적으로 개발되었으며, Solar LLM API와 RAG 시스템의 실무 적용 사례를 보여줍니다.
