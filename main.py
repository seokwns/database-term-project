import psycopg2
from user.service import UserService

if __name__ == '__main__':
    connection = psycopg2.connect(
        database='sample2023',
        user='seokjun',
        password='qwer1234',
        host='::1',
        port='5432'
    )

    cursor = connection.cursor()

    user_service = UserService(connection, cursor)

    while True:
        print()
        print("------------------------------")
        print()
        print("mat-zip")
        print("1. 회원가입")
        print("2. 로그인")
        print("3. 맛집 검색하기")
        print("4. 좋아요 목록 보기")
        print("5. 작성한 리뷰 보기")
        print("6. Exit")
        print()
        print("------------------------------")
        print()

        itr = int(input("> "))

        if itr == 1:
            print()
            print("------------------------------")
            print()
            print("[ 회원가입 ]")
            print()
            print("회원가입 정보를 기입해주세요.")
            print()
            print("------------------------------")
            print()

            email = input("email: ")
            name = input("name: ")
            password = input("password: ")

            user_service.register(email, name, password)

            print()
            print("------------------------------")
            print()
            print("[ 회원가입 ]")
            print()
            print("회원가입 완료!")
            print()
            print("------------------------------")
            print()

        elif itr == 2:
            print()
            print("------------------------------")
            print()
            print("[ 로그인 ]")
            print()
            print("로그인 정보를 입력해주세요.")
            print()
            print("------------------------------")
            print()

            email = input("email: ")
            password = input("password: ")

            logined = user_service.login(email, password)

            if logined:
                print()
                print("------------------------------")
                print()
                print("[ 로그인 완료 ]")
                print()
                print("------------------------------")
                print()
            else:
                print()
                print("------------------------------")
                print()
                print("[ 로그인 실패 ]")
                print()
                print("비밀번호가 틀렸거나 존재하지 않는 계정입니다.")
                print()
                print("------------------------------")
                print()

        elif itr == 3:
            print()
        elif itr == 4:
            print()
            print()
            print("Bye")
            break

    cursor.close()
    connection.close()