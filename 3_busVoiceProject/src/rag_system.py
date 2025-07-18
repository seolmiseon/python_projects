import os
from langchain_upstage import UpstageEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.utils import get_from_env
from dotenv import load_dotenv
import json
import time

load_dotenv()

# Solar Embeddings 설정 - 지연 초기화
embeddings = None

UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY")
if not UPSTAGE_API_KEY:
    raise ValueError("UPSTAGE_API_KEY not found in environment variables")

embeddings = UpstageEmbeddings(model="solar-embedding-1-large")

class BusRAGSystem:
    def __init__(self):
        self.vectorstore = None
        self.chunk_experiments = []
        
    def create_bus_documents(self):
        """
        버스 관련 문서 데이터 생성
        """
        bus_documents = [
            {
                "content": "시내버스는 도시 내 주요 지역을 연결하는 대중교통수단입니다. 배차간격은 보통 10-20분이며, 출퇴근 시간에는 더 자주 운행됩니다.",
                "metadata": {"type": "bus_info", "category": "시내버스", "info": "기본정보"}
            },
            {
                "content": "시외버스는 도시 간 이동을 위한 장거리 버스입니다. 배차간격이 길고, 예약이 필요한 경우가 많습니다.",
                "metadata": {"type": "bus_info", "category": "시외버스", "info": "기본정보"}
            },
            {
                "content": "출근시간(07:00-09:00)에는 버스가 매우 혼잡하며, 배차간격이 짧아집니다. 시각장애인은 안전을 위해 다른 승객의 도움을 받는 것이 좋습니다.",
                "metadata": {"type": "bus_info", "category": "시간대", "info": "출근시간"}
            },
            {
                "content": "퇴근시간(18:00-20:00)에도 버스가 혼잡하며, 특히 지하철역 근처 정류장에서는 승객이 많습니다.",
                "metadata": {"type": "bus_info", "category": "시간대", "info": "퇴근시간"}
            },
            {
                "content": "첫차는 보통 새벽 5시경에 운행을 시작하며, 막차는 밤 12시경에 운행을 종료합니다. 정확한 시간은 노선마다 다릅니다.",
                "metadata": {"type": "bus_info", "category": "운행시간", "info": "첫차막차"}
            },
            {
                "content": "마을버스는 주로 주거지역 내 이동을 위한 소형 버스입니다. 배차간격이 길고, 노선이 복잡할 수 있습니다.",
                "metadata": {"type": "bus_info", "category": "마을버스", "info": "기본정보"}
            }
        ]
        return bus_documents
    
    def create_vectorstore_with_chunk_size(self, chunk_size=500, chunk_overlap=50):
        """
        지정된 청크 크기로 벡터스토어 생성
        """
        documents = self.create_bus_documents()
        
        # 텍스트 분할
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
        
        docs = []
        for doc in documents:
            splits = text_splitter.split_text(doc["content"])
            for split in splits:
                docs.append(Document(
                    page_content=split,
                    metadata=doc["metadata"]
                ))
        
        # ChromaDB 벡터스토어 생성
        vectorstore = Chroma.from_documents(
            documents=docs,
            embedding=embeddings
        )
        
        return vectorstore, len(docs)
    
    def test_chunk_sizes(self):
        """
        다양한 청크 크기로 실험 수행
        """
        chunk_sizes = [100, 200, 300, 500, 1000]
        test_question = "출근시간에 시내버스를 이용할 때 주의사항은 무엇인가요?"
        
        print("=== 청크 크기별 실험 시작 ===")
        
        for chunk_size in chunk_sizes:
            print(f"\n--- 청크 크기: {chunk_size} ---")
            
            # 벡터스토어 생성
            start_time = time.time()
            vectorstore, doc_count = self.create_vectorstore_with_chunk_size(chunk_size)
            creation_time = time.time() - start_time
            
            # 검색 테스트
            start_time = time.time()
            results = vectorstore.similarity_search(test_question, k=3)
            search_time = time.time() - start_time
            
            # 결과 평가
            relevance_score = self.evaluate_relevance(results, test_question)
            
            experiment_result = {
                "chunk_size": chunk_size,
                "document_count": doc_count,
                "creation_time": creation_time,
                "search_time": search_time,
                "relevance_score": relevance_score,
                "results": [doc.page_content for doc in results]
            }
            
            self.chunk_experiments.append(experiment_result)
            
            print(f"문서 수: {doc_count}")
            print(f"생성 시간: {creation_time:.3f}초")
            print(f"검색 시간: {search_time:.3f}초")
            print(f"관련성 점수: {relevance_score:.2f}")
            print(f"검색 결과: {[doc.page_content[:50] + '...' for doc in results]}")
        
        return self.chunk_experiments
    
    def evaluate_relevance(self, results, question):
        """
        검색 결과의 관련성 평가 (간단한 키워드 기반)
        """
        question_keywords = ["출근시간", "시내버스", "주의사항", "혼잡"]
        total_score = 0
        
        for doc in results:
            content = doc.page_content.lower()
            score = sum(1 for keyword in question_keywords if keyword in content)
            total_score += score
        
        return total_score / len(results) if results else 0
    
    def get_best_chunk_size(self):
        """
        실험 결과를 바탕으로 최적의 청크 크기 반환
        """
        if not self.chunk_experiments:
            return 500  # 기본값
        
        # 관련성 점수가 가장 높은 청크 크기 선택
        best_experiment = max(self.chunk_experiments, key=lambda x: x["relevance_score"])
        return best_experiment["chunk_size"]
    
    def setup_optimal_rag(self):
        """
        최적의 청크 크기로 RAG 시스템 설정
        """
        if not self.chunk_experiments:
            self.test_chunk_sizes()
        
        best_chunk_size = self.get_best_chunk_size()
        print(f"최적 청크 크기: {best_chunk_size}")
        
        self.vectorstore, _ = self.create_vectorstore_with_chunk_size(best_chunk_size)
        return self.vectorstore
    
    def search_bus_info(self, query, k=3):
        """
        버스 관련 정보 검색
        """
        if not self.vectorstore:
            self.vectorstore = self.setup_optimal_rag()
        
        if self.vectorstore is None:
            return []
        
        results = self.vectorstore.similarity_search(query, k=k)
        return results
    
    def save_experiment_results(self, filename="chunk_experiments.json"):
        """
        실험 결과를 JSON 파일로 저장
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.chunk_experiments, f, ensure_ascii=False, indent=2)
        print(f"실험 결과가 {filename}에 저장되었습니다.")

# 전역 RAG 시스템 인스턴스
rag_system = BusRAGSystem() 