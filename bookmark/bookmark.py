class Bookmark:
    def __init__(self, record):
        self.url = record[1]
        self.title = record[2]
        self.memo_content = record[8] if record[8] is not None else None
        self.memo_created_at = record[9] if record[9] is not None else None
