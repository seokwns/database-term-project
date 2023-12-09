class MemoService:
    def __init__(self, memo_repository):
        self.memo_repository = memo_repository

    def save(self, user_id, bookmark_id, content):
        self.memo_repository.save(user_id, bookmark_id, content)

    def update(self, user_id, url, content):
        self.memo_repository.update(user_id, url, content)
