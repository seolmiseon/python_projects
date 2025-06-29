from collections import Counter

class TextAnalyzer:
    def __init__(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            self.text = f.read()

    def word_count(self):
        return len(self.text.split())

    def most_common_word(self):
        from collections import Counter
        words = self.text.split()
        return Counter(words).most_common(1)[0]
    
    def count_specific_word(self, target_word):
        return self.text.split().count(target_word) 
    
## 1. 위에서 구현했던 TextAnalyzer 상속받아서 AdvancedTextAnalyzer 만들기
class AdvancedTextAnalyzer(TextAnalyzer):
    ## 2. AdvancedTextAnalyzer 클래스에 메서드 longest_word 구현하기
    def longest_word(self):
        words = self.text.split()
        return max(words, key=len)
    
    # 2. word_count_with_target 수정, target_word 를 받아와야함
    def word_count_with_target(self,target_word):
        # 3. super 를 활용하여 기존 메서드 (word_count) 불러와 수정하기
        total = super().word_count()
        count = self.text.split().count(target_word)
        return total, count
    def word_refresh(self, n=None):
        words = self.text.split()
        word_counts = Counter(words)
        sorted_words =  sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_words[:n] if n is not None else sorted_words
    
