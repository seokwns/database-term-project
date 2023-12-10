from .history import History


class HistoryService:
    def __init__(self, history_repository):
        self.history_repository = history_repository

    def save(self, user_id, keyword, page):
        if user_id == -1:
            return

        return self.history_repository.save(user_id, keyword, page)

    def find_by_user_id(self, user_id, page):
        results, count = self.history_repository.find_by_user_id(user_id, page)

        histories = []
        for result in results:
            histories.append(History(result[1], result[2], result[3], result[4]))

        return histories, count[0]

    def find_by_user_id_and_keyword(self, user_id, keyword, page):
        results, count = self.history_repository.find_by_user_id_and_keyword(user_id, keyword, page)

        histories = []
        for result in results:
            histories.append(History(result[1], result[2], result[3], result[4]))

        return histories, count[0]
