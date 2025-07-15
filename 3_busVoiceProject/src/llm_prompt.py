from transformers.pipelines import pipeline
import re


noticeWord = pipeline("text-generation", model="skt/kogpt2-base-v2")
def generate_notice_word(bus_number:str) -> str:
    prompt = f"{bus_number}번 버스가 도착했습니다. (이 문장만 출력하세요. 아무 말도 덧붙이지 마세요.)"
    try:
        response = noticeWord(prompt, max_length=20, num_return_sequences=1)
        text = response[0]["generated_text"]
        match = re.search(r"(\d+번 버스가 도착했습니다\.)", text)
        if match:
            return match.group(0)
        else:
            return f"이 버스는 {bus_number}번 버스입니다."
    except Exception as e:
        print(f"오류 발생: {e}")
        return f"이 버스는 {bus_number}번 버스입니다."
  

