from .user_utils import Utils


class UserService:

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def register(self, email, name, password):
        email_exists = self.user_repository.check_email_exists(email)

        if email_exists is False:
            print("이미 존재하는 이메일입니다. 다른 이메일을 사용해주세요.")
            return False

        if Utils.is_email(email) is False:
            print("이메일 형식으로 작성해주세요.")
            return False

        if Utils.check_password_complexity(password) is False:
            print("비밀번호 형식을 지켜주세요.")
            return False

        if Utils.check_name_length(name) is False:
            print("이름 형식을 지켜주세요.")
            return False

        self.user_repository.save_user(email, name, password)
        return True

    def login(self, email, password):
        entity = self.user_repository.find_user_by_email(email)

        if entity is False:
            return -1

        if entity.password == password:
            return entity.id

        return -1

    def delete(self, user_id):
        return self.user_repository.delete_user(user_id)
