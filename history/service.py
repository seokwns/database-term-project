from .repository import HistoryRepository
from .history import History


class HistoryService:
    def __init__(self, connection, cursor):
        self.history_repository = HistoryRepository(connection, cursor)

    def save(self, user_id, keyword, page):
        return self.history_repository.save(user_id, keyword, page)

    def find_by_user_id(self, user_id, page):
        results = self.history_repository.find_by_user_id(user_id, page)

        print(results)

        histories = []
        for result in results:
            histories.append(History(result[1], result[2], result[3], result[4]))

        return histories

    def find_by_user_id_and_keyword(self, user_id, keyword, page):
        results = self.history_repository.find_by_user_id_and_keyword(user_id, keyword, page)

        print(results)

        histories = []
        for result in results:
            histories.append(History(result[1], result[2], result[3], result[4]))

        return histories
