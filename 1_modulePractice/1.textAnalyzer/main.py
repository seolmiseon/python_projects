from anlalizer import TextAnalyzer, AdvancedTextAnalyzer

# test.txt 생성
with open('test.txt', 'w', encoding='utf-8') as f:
    f.write("hello world hello python world hello")
  # TextAnalyzer 클래스 정의
 
    
analyzer = TextAnalyzer('test.txt')
print("총 단어 수:", analyzer.word_count())
print("가장 많이 나온 단어:", analyzer.most_common_word())
print("hello 단어 수:", analyzer.count_specific_word('hello'))



##  새로운 객체 만들기
advanced_analyzer = AdvancedTextAnalyzer('test.txt')
print("가장 긴 단어:", advanced_analyzer.longest_word())
print("전체 단어 수 + 'hello' 횟수:", advanced_analyzer.word_count_with_target('hello'))
print("단어 빈도 (상위 3개):", advanced_analyzer.word_refresh(3))
