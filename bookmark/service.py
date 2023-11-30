from .repository import BookmarkRepository
from .bookmark import Bookmark


class BookmarkService:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
        self.bookmark_repository = BookmarkRepository(connection, cursor)

    def save(self, post, user_id):
        if user_id < 1:
            print("로그인을 후 이용 가능합니다.")
            print("로그인을 해주세요.")
            return None

        self.bookmark_repository.save(post, user_id)

    def find(self, user_id, page):
        if user_id < 1:
            print("로그인을 후 이용 가능합니다.")
            print("로그인을 해주세요.")
            return None

        responses = self.bookmark_repository.find(user_id, page)
        dtos = []

        for response in responses:
            dtos.append(Bookmark(response))

        return dtos
