from langchain_upstage import ChatUpstage
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from model_utils import get_solar_mini, get_solar_pro
from config import config
import os 


def setup_rag_chain(retriever):
    
    chat_mini = get_solar_mini(config.UPSTAGE_API_KEY)
    chat_pro = get_solar_pro(config.UPSTAGE_API_KEY)
    
    #solar_mini를 사용한 질문 분류 
    classify_prompt = ChatPromptTemplate.from_template("다음 질문을 분류하세요: {input}")
    
    
    #solar_pro를 사용
    contextualize_q_prompt = ChatPromptTemplate.from_messages([
         ("system", "이전 대화 내용과 최신 사용자 질문이 있을 때, 이 질문이 이전 대화 내용과 관련이 있을 수 있습니다. 이런 경우, 대화 내용을 알 필요 없이 독립적으로 이해할 수 있는 질문으로 바꾸세요. 질문에 답할 필요는 없고, 필요하다면 그저 다시 구성하거나 그대로 두세요."),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    history_aware_retriever = create_history_aware_retriever(chat_pro,retriever, contextualize_q_prompt)
    
    qa_prompt = ChatPromptTemplate.from_messages([
         ("system", "질문-답변 업무를 돕는 보조원입니다. 질문에 답하기 위해 검색된 내용을 사용하세요. 답을 모르면 모른다고 말하세요. 답변은 세 문장 이내로 간결하게 유지하세요.\n## 답변 예시\n📍답변 내용:\n📍증거:\n{context}"),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    
    question_answer_chain = create_stuff_documents_chain(chat_pro, qa_prompt)
    
    # 두 모델 결합 
    def combined_chain(input_data):
        classification = chat_mini.invoke(classify_prompt.format_messages(input=input_data["input"]))
        rag_result = create_retrieval_chain(history_aware_retriever, question_answer_chain).invoke(input_data)
        
        final_result = {
            "classification": classification.content,
            "answer": rag_result["answer"],
            "context": rag_result.get("context", "")
        }
        return final_result
    return combined_chain