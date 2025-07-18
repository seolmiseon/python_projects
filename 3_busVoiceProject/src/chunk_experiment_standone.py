from rag_system import rag_system

if __name__ == "__main__":
    print("청크 크기 실험 시작..")
    rag_system.test_chunk_sizes()
    rag_system.save_experiment_results()
    print("실험 완료")