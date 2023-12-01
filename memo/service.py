from .repository import MemoRepository


class MemoService:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
        self.memo_repository = MemoRepository(connection, cursor)

    def save(self, user_id, bookmark_id, content):
        self.memo_repository.save(user_id, bookmark_id, content)

    def update(self, user_id, url, content):
        self.memo_repository.update(user_id, url, content)
