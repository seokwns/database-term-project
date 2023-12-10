import psycopg2
import joblib
from konlpy.tag import Mecab

from utils import Utils

from user.repository import UserRepository
from bookmark.repository import BookmarkRepository
from memo.repository import MemoRepository
from history.repository import HistoryRepository

from user.controller import UserController
from search.controller import SearchController
from bookmark.controller import BookmarkController
from history.controller import HistoryController

from user.service import UserService
from bookmark.service import BookmarkService
from memo.service import MemoService
from history.service import HistoryService


mecab = Mecab()


def mecab_tokenizer(text):
    return mecab.morphs(text)


if __name__ == '__main__':
    connection = psycopg2.connect(
        database='sample2023',
        user='seokjun',
        password='qwer1234',
        host='::1',
        port='5432'
    )

    count_vector = joblib.load('search/machine/count_vectorizer.pkl')
    logistic_regression = joblib.load('search/machine/logistic_regression.pkl')

    cursor = connection.cursor()

    user_repository = UserRepository(connection, cursor)
    bookmark_repository = BookmarkRepository(connection, cursor)
    memo_repository = MemoRepository(connection, cursor)
    history_repository = HistoryRepository(connection, cursor)

    user_service = UserService(user_repository)
    bookmark_service = BookmarkService(bookmark_repository)
    memo_service = MemoService(memo_repository)
    history_service = HistoryService(history_repository)

    user_controller = UserController(connection, cursor, user_service)
    search_controller = SearchController(connection, cursor, bookmark_service, memo_service, history_service, count_vector, logistic_regression)
    bookmark_controller = BookmarkController(connection, cursor, bookmark_service, memo_service)
    history_controller = HistoryController(connection, cursor, history_service)

    user_id = -1

    while True:

        if user_id < 0:
            print("+-------------------------------------------------+")
            print("|                  see-realview                   |")
            print("+-------------------------------------------------+")
            print("|  1. 회원가입                                    |")
            print("|  2. 로그인                                      |")
            print("|  3. 맛집 검색하기                               |")
            print("|  4. Exit                                        |")
            print("+-------------------------------------------------+")
        else:
            print("+-------------------------------------------------+")
            print("|                  see-realview                   |")
            print("+-------------------------------------------------+")
            print("|  1. 로그아웃                                    |")
            print("|  2. 맛집 검색하기                               |")
            print("|  3. 북마크 목록                                 |")
            print("|  4. 검색 기록 보기                              |")
            print("|  5. 회원 탈퇴                                   |")
            print("|  6. Exit                                        |")
            print("+-------------------------------------------------+")

        main_menu_iterator = Utils.get_main_menu_iterator(user_id)

        if user_id > 0 and main_menu_iterator == 1:
            user_id = -1
            print("로그아웃 완료")

        elif user_id < 0 and main_menu_iterator == 1:
            user_controller.register()

        elif user_id < 0 and main_menu_iterator == 2:
            user_id = user_controller.login()

        elif (user_id < 0 and main_menu_iterator == 3) or (user_id > 0 and main_menu_iterator == 2):
            search_controller.search(user_id)

        elif user_id > 0 and main_menu_iterator == 3:
            while True:
                print("+-------------------------------------------------+")
                print("|                   북마크 목록                   |")
                print("+-------------------------------------------------+")
                print("|  1. 목록 보기                                   |")
                print("|  2. 최근에 추가한 순서로 보기                   |")
                print("|  3. 제목에서 검색하기                           |")
                print("|  4. 제목과 메모에서 검색하기                    |")
                print("|  5. 뒤로가기                                    |")
                print("+-------------------------------------------------+")

                bookmark_menu_iterator = Utils.get_integer(5)

                if bookmark_menu_iterator == 1 or bookmark_menu_iterator == 2:
                    bookmark_controller.find_bookmarks(user_id, bookmark_menu_iterator)

                elif bookmark_menu_iterator == 3 or bookmark_menu_iterator == 4:
                    bookmark_controller.find_filtered_bookmark(user_id, bookmark_menu_iterator)

                elif bookmark_menu_iterator == 5:
                    break

        elif user_id > 0 and main_menu_iterator == 4:
            page = 0
            while True:
                print("+-------------------------------------------------+")
                print("|                  검색기록 메뉴                  |")
                print("+-------------------------------------------------+")
                print("|  1. 기록 보기                                   |")
                print("|  2. 키워드로 검색하기                           |")
                print("|  3. 뒤로가기                                    |")
                print("+-------------------------------------------------+")

                history_menu_iterator = Utils.get_integer(3)

                if history_menu_iterator == 1 or history_menu_iterator == 2:
                    history_controller.find_histories(user_id, history_menu_iterator)

                elif history_menu_iterator == 3:
                    break

        elif user_id > 0 and main_menu_iterator == 5:
            print("+-------------------------------------------------+")
            print("|                    회원 탈퇴                    |")
            print("+-------------------------------------------------+")
            print("|  1. Yes                                         |")
            print("|  2. No                                          |")
            print("+-------------------------------------------------+")

            delete_menu_iterator = Utils.get_integer(2)

            if delete_menu_iterator == 1:
                user_id = user_controller.withdraw(user_id)

        elif (user_id < 0 and main_menu_iterator == 4) or (user_id > 0 and main_menu_iterator == 6):
            print("+-------------------------------------------------+")
            print("|                       Bye                       |")
            print("+-------------------------------------------------+")
            break

    cursor.close()
    connection.close()
