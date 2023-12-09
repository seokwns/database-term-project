from .service import UserService


class UserController:
    def __init__(self, connection, cursor, user_service):
        self.connection = connection
        self.cursor = cursor
        self.user_service = user_service

    def register(self):
        print("+---------------------------------------------------------------------------------+")
        print("|                                    회원가입                                     |")
        print("+---------------------------------------------------------------------------------+")
        print("|  회원가입 정보를 기입해주세요.                                                  |")
        print("|  - 이름은 2글자 이상, 10글자 이하만 가능합니다.                                 |")
        print("|  - 비밀번호는 영문자, 숫자, 특수문자 포함 8글자 이상, 30글자 이하만 가능합니다. |")
        print("|  - 회원가입을 취소할 경우, \quit을 입력해주세요.                                |")
        print("+---------------------------------------------------------------------------------+")

        while True:
            email = input(" > email: ")
            if email == '\\quit':
                break

            name = input(" > name: ")
            if name == '\\quit':
                break

            password = input(" > password: ")
            if password == '\\quit':
                break

            registered = self.user_service.register(email, name, password)

            if registered is True:
                print("+--------------------------------------------------------------------------------+")
                print("|                                 회원가입 완료                                  |")
                print("+--------------------------------------------------------------------------------+")
                break

    def login(self):
        print("+-------------------------------------------------+")
        print("|                     로그인                      |")
        print("+-------------------------------------------------+")
        print("|  로그인 정보를 입력해주세요.                    |")
        print("|  이메일에 \quit을 입력하면 메뉴로 돌아갑니다.   |")
        print("+-------------------------------------------------+")
        email = input(" > email: ")
        if email == '\\quit':
            return -1

        password = input(" > password: ")

        user_id = self.user_service.login(email, password)

        if user_id > 0:
            print("+-------------------------------------------------+")
            print("|                   로그인 완료                   |")
            print("+-------------------------------------------------+")
        else:
            print("+-------------------------------------------------+")
            print("|                   로그인 실패                   |")
            print("+-------------------------------------------------+")
            print("|  비밀번호가 틀리거나 존재하지 않는 계정입니다.  |")
            print("+-------------------------------------------------+")

        return user_id

    def withdraw(self, user_id):
        deleted = self.user_service.delete(user_id)
        if deleted is True:
            return -1
            print("+-------------------------------------------------+")
            print("|                    탈퇴 완료                    |")
            print("+-------------------------------------------------+")
        else:
            print("+-------------------------------------------------+")
            print("|       탈퇴 과정에서 오류가 발생했습니다.        |")
            print("+-------------------------------------------------+")
            return user_id
