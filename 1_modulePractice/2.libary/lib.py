import os

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __str__(self):
        return f"제목: {self.title}, 저자: {self.author}"


class BaseLibrary:
    def __init__(self):
        self.books = []

    def add_book(self, title, author):
        self.books.append(Book(title, author))
        print("✅ 책이 추가되었습니다.")

    def remove_book(self, title):
        self.books = [b for b in self.books if b.title != title]
        print("🗑️ 삭제 시도 완료")

    def search_book(self, title):
        for b in self.books:
            if b.title == title:
                return b  # Book 객체 반환
    
        return None
    def list_books(self):
        if not self.books:
            print("📚 등록된 책이 없습니다.")
        else:
            print("📚 도서 목록:")
            for book in self.books:
                print(book)

    
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
class AuthLibrary(BaseLibrary):
    def __init__(self):
        super().__init__()
        self.users = []

    # 3. 유저 정보 찾는 함수 만들기 (find_user)
    def find_user(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None # 모든 유저정보에 대해 매칭이 안될때 None 반환

    # 4. 유저 등록 함수 만들기 (register_user)
    def register_user(self, username, password):
        if self.find_user(username):
            return False
        self.users.append(User(username, password))
        return True

    # 5. 로그인 함수 만들기 (login)
    def login(self, username, password):
        user = self.find_user(username)
        if user and user.password == password:
            return True
        else:
            return False        

# 1. 로그인기능이 있는 AuthLibrary 상속받아 대출 기능 추가한 LonLibrary 만들기
class LoanLibrary(AuthLibrary):
    def __init__(self):
        super().__init__()
        self.loans = {}    # {username: [Book, ...]}

    # 2. 책 빌리는 행위를 함수로 만들어주기 : 유저, 책정보
    def borrow_book(self, username, title):
        if not self.find_user(username):
            print("❌ 사용자를 찾을수 없습니다.")
            return
        book = self.search_book(title)
        if book:
            if book in self.books:        
                self.books.remove(book)
                self.loans.setdefault(username, []).append(book)
                print("📦 대출 완료")
            else:
                print(f"❌ '{title}'은(는) 이미 대출된 책입니다.")
        else:
            print(f"❌ '{title}' 책을 찾을 수 없습니다.")

    # 3. 책을 반납받는 행위 함수로 만들어주기 : 유저, 책정보
    def return_book(self, username, title):
        if username not in self.loans:
            print("❌ 대출 기록 없음")
            return None  # 함수 종료 (None 반환)

        for book in self.loans.get(username, []):
            if book.title == title:
                self.loans[username].remove(book)
                self.books.append(book)
                print("📥 반납 완료")
                return None # 함수 종료 (None 반환)
        print("❌ 반납 대상 아님")
        
    def list_loans(self):
        if not self.loans:
            print("📚 대출된 책이 없습니다.")
        else:
            print("📚 대출 목록:")
            for username, books in self.loans.items():
                print(f"{username}의 대출 도서:")
                for book in books:
                    print(f"  - {book}")
                
# 1. 대출 기능 추가한 LonLibrary 상속받아서 기록 관리하는 FileLibrary 만들기
class FileLibrary(LoanLibrary):
    # 2. 현재 존재하는 책, 유저, 대출 정보 txt file 로 저장하기
    # with, open 어쩌구는 일단 "그림"이라 생각하고 읽어주세요. 금욜에 배웁니다.
    def save_all(self):
        # books.txt 라는 곳에 현재 도서관에 존재하는 books 데이터 저장
        with open("books.txt", "w", encoding="utf-8") as f:
            for b in self.books:
                f.write(f"{b.title}|{b.author}\n")
        # users.txt 라는 곳에 현재 도서관에 존재하는 users 데이터 저장
        with open("users.txt", "w", encoding="utf-8") as f:
            for u in self.users:
                f.write(f"{u.username}|{u.password}\n")
        # loans.txt 라는 곳에 현재 도서관에 존재하는 loans 데이터 저장
        with open("loans.txt", "w", encoding="utf-8") as f:
            for u, blist in self.loans.items():
                titles = ",".join([b.title for b in blist])
                f.write(f"{u}:{titles}\n")

    # 3. 저장했던 txt file 들로 부터 데이터 불러오기.
    def load_all(self):
        # 해당 txt file 이 존재하는 지 체크
        if os.path.exists("books.txt"):
            with open("books.txt", "r", encoding="utf-8") as f:
                for line in f:
                    t, a = line.strip().split("|")
                    self.add_book(t, a)

        if os.path.exists("users.txt"):
            with open("users.txt", "r", encoding="utf-8") as f:
                for line in f:
                    uid, pw = line.strip().split("|")
                    self.register_user(uid, pw)

        if os.path.exists("loans.txt"):
            with open("loans.txt", "r", encoding="utf-8") as f:
                for line in f:
                    uid, titles = line.strip().split(":")
                    if titles:
                        for t in titles.split(","):
                            book = next((b for b in self.books if b.title == t), None)
                            if book:
                                self.books.remove(book)
                                self.loans.setdefault(uid, []).append(book)                