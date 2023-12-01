import re


class Utils:

    @staticmethod
    def is_email(email):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_pattern, email) is not None

    @staticmethod
    def check_password_complexity(password):
        # 최소 8자리 최대 30자리
        if not (8 <= len(password) <= 30):
            return False

        # 영문자, 숫자, 특수문자 모두 포함
        if not (re.search(r'[a-zA-Z]', password) and
                re.search(r'\d', password) and
                re.search(r'[!@#$%^&*]', password)):
            return False

        # 특수문자 1개 이상 포함
        if not re.search(r'[!@#$%^&*]', password):
            return False

        # 모든 조건을 만족하면 True 반환
        return True

    @staticmethod
    def check_name_length(name):
        return 2 <= len(name) <= 10
