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

        return self.bookmark_repository.save(post, user_id)

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

    def find_order_by_date(self, user_id, page):
        if user_id < 1:
            print("로그인을 후 이용 가능합니다.")
            print("로그인을 해주세요.")
            return None

        responses = self.bookmark_repository.find_order_by_date(user_id, page)
        dtos = []

        for response in responses:
            dtos.append(Bookmark(response))

        return dtos

    def find_all_by_urls_in(self, urls):
        return self.bookmark_repository.find_all_by_urls_in(urls)

    def find_in_title(self, user_id, keyword):
        if user_id < 1:
            print("로그인을 후 이용 가능합니다.")
            print("로그인을 해주세요.")
            return None

        responses = self.bookmark_repository.find_in_title(user_id, keyword)
        dtos = []

        for response in responses:
            dtos.append(Bookmark(response))

        return dtos

    def find_in_title_and_memo(self, user_id, keyword):
        if user_id < 1:
            print("로그인을 후 이용 가능합니다.")
            print("로그인을 해주세요.")
            return None

        if len(keyword) == 0:
            print("키워드를 입력해주세요.")
            return None

        responses = self.bookmark_repository.find_in_title_and_memo(user_id, keyword)
        dtos = []

        for response in responses:
            dtos.append(Bookmark(response))

        return dtos

    def delete(self, user_id, url):
        if user_id < 1:
            print("로그인을 후 이용 가능합니다.")
            print("로그인을 해주세요.")
            return None

        self.bookmark_repository.delete(user_id, url)
