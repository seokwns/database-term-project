import math

from utils import Utils


class HistoryController:
    def __init__(self, connection, cursor, history_service):
        self.connection = connection
        self.cursor = cursor
        self.history_service = history_service

    def find_histories(self, user_id, history_menu_iter):
        page = 0
        max_page = 0
        while True:
            histories = []

            if history_menu_iter == 1:
                histories, count = self.history_service.find_by_user_id(user_id, page)
            elif history_menu_iter == 2:
                history_keyword = input(" > keyword : ")
                print()
                histories, count = self.history_service.find_by_user_id_and_keyword(user_id, history_keyword, page)

            max_page = math.ceil(count / 10)

            for (idx, value) in enumerate(histories):
                print(f'   {idx + 1}.')
                print("      키워드 =", value.keyword)
                print("      페이지 =", value.page)
                print("      날짜 =", value.searched_at)
                print()

            print("+-------------------------------------------------+")
            print("|                  검색기록 메뉴                  |")
            print("+-------------------------------------------------+")
            print("|  1. 다음 페이지 보기                            |")
            print("|  2. 이전 페이지 보기                            |")
            print("|  3. 뒤로가기                                    |")
            print("+-------------------------------------------------+")

            history_menu_iter2 = Utils.get_integer(3)

            if history_menu_iter2 == 1:
                page += 1
                if page > max_page:
                    page -= 1
                    print("+-------------------------------------------------+")
                    print("|  마지막 페이지 입니다.                          |")
                    print("+-------------------------------------------------+")

            elif history_menu_iter2 == 2:
                page -= 1
                if page < 0:
                    page = 0
                    print("+-------------------------------------------------+")
                    print("|  첫번째 페이지 입니다.                          |")
                    print("+-------------------------------------------------+")

            elif history_menu_iter2 == 3:
                break
