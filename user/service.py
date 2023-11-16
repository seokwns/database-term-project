from .repository import UserRepository
from .utils import Utils


class UserService:

    def __init__(self, connection, cursor):
        self.user_repository = UserRepository(connection, cursor)

    def register(self, email, name, password):
        email_exists = self.user_repository.check_email_exists(email)

        if email_exists is False:
            print("이미 존재하는 이메일입니다. 다른 이메일을 사용해주세요.")
            return

        if Utils.is_email(email) is False:
            print("이메일 형식으로 작성해주세요.")
            return

        self.user_repository.saveUser(email, name, password)

    def login(self, email, password):
        entity = self.user_repository.findUserByEmail(email)

        if entity is False:
            return False

        if entity.password == password:
            return True

        return False
