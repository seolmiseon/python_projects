from lib import FileLibrary
   
            
def main():
    lib = FileLibrary()
    lib.load_all()
    
    if not lib.books:
        lib.add_book("한강", "조정래")
        lib.add_book("총, 균, 쇠", "재레드 다이아몬드")
        lib.add_book("작은 것이 아름답다", "E.F. 슈마허")
        lib.save_all()
        
    current_user = None
    
    while not current_user:
         print("\n1. 로그인  2. 회원가입  3. 종료")
         cmd = input("선택: ")
         if cmd == '1':
            uid = input("아이디: ")
            pw = input("비밀번호: ")
            if lib.login(uid, pw):
                current_user = uid
                print("✅ 로그인 성공")
            else:
                print("❌ 실패")
         elif cmd == '2':
            uid = input("아이디 생성: ")
            pw = input("비번 생성: ")
            if lib.register_user(uid, pw):
                print("✅ 회원가입 완료")
            else:
                print("❌ 이미 존재하는 아이디입니다.")
         else:
            return

    while True:
        print("\n1. 책 추가 2. 삭제 3. 검색 4. 목록 5. 대출 목록 6. 책 대출 7. 책 반납 8. 종료")
        sel = input("선택: ")
        if sel == '1':
            lib.add_book(input("제목: "), input("저자: "))
        elif sel == '2':
            lib.remove_book(input("제목: "))
        elif sel == '3':
             result = lib.search_book(input("제목: "))
             if result:
                 print(f"검색 결과: {result}")
             else:
                 print("책을 찾을 수 없습니다.")
        elif sel == '4':
            lib.list_books()
        elif sel == '5':
            lib.list_loans()
        elif sel == '6':
            if current_user:
                lib.borrow_book(current_user, input("대출할 책 제목: "))
        elif sel == '7':
            if current_user:
                lib.return_book(current_user, input("반납할 책 제목: "))
        elif sel == '8':
            break
        lib.save_all()    
if __name__ == "__main__":
    main()        
