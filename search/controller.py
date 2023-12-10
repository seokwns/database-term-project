import webbrowser

from search.naver import search_keyword
from utils import Utils


class SearchController:
    def __init__(self, connection, cursor, bookmark_service, memo_service, history_service, vectorizer, model):
        self.connection = connection
        self.cursor = cursor
        self.bookmark_service = bookmark_service
        self.memo_service = memo_service
        self.history_service = history_service
        self.vectorizer = vectorizer
        self.model = model

    @staticmethod
    def format_date_string(input_string):
        if len(input_string) == 8:
            formatted_date = f'{input_string[:4]}-{input_string[4:6]}-{input_string[6:]}'
            return formatted_date
        else:
            return input_string

    def search(self, user_id):
        keyword = ""
        number = 1

        print("+-------------------------------------------------+")
        print("|                   맛집 검색                     |")
        print("+-------------------------------------------------+")
        print("|  키워드를 입력해주세요.                         |")
        print("+-------------------------------------------------+")

        while True:
            try:
                keyword = input(" > keyword: ")
                number = int(input(" > 페이지: "))
                if 1 <= number:
                    break
                else:
                    print("+-------------------------------------------------+")
                    print("|  페이지는 1 이상의 숫자만 입력해주세요.         |")
                    print("+-------------------------------------------------+")
            except ValueError:
                print("+-------------------------------------------------+")
                print("|  페이지는 1 이상의 숫자만 입력해주세요.         |")
                print("+-------------------------------------------------+")
                continue

        while True:
            print("+-------------------------------------------------+")
            print("|  검색 중 입니다. 잠시만 기다려주세요...         |")
            print("+-------------------------------------------------+")
            print()
            self.history_service.save(user_id, keyword, number)
            search_response = search_keyword(keyword, number, self.vectorizer, self.model)

            urls = []

            for response in search_response:
                urls.append(response.link)

            bookmarks = self.bookmark_service.find_all_by_urls_in(urls)

            self.display_search_responses(bookmarks, search_response)

            go_back = False

            while True:
                print("+-------------------------------------------------+")
                print("|                    검색 메뉴                    |")
                print("+-------------------------------------------------+")
                print("|  1. 다음 페이지 보기                            |")
                print("|  2. 이전 페이지 보기                            |")
                print("|  3. URL 열기                                    |")
                print("|  4. 북마크 추가하기                             |")
                print("|  5. 뒤로가기                                    |")
                print("+-------------------------------------------------+")
                search_menu_iterator = Utils.get_integer(5)

                if search_menu_iterator == 1:
                    number += 1
                    break

                elif search_menu_iterator == 2:
                    number -= 1
                    if number < 0:
                        number = 0
                    break

                elif search_menu_iterator == 3:
                    self.open_url(search_response)

                elif search_menu_iterator == 4:
                    if user_id > 0:
                        self.save_bookmark(search_response, user_id)
                    else:
                        print("+-------------------------------------------------+")
                        print("|         로그인이 필요한 서비스 입니다.          |")
                        print("+-------------------------------------------------+")

                elif search_menu_iterator == 5:
                    go_back = True
                    break

            if go_back is True:
                break

    def save_bookmark(self, search_response, user_id):
        print("+-------------------------------------------------+")
        print("|          포스트 번호를 입력해주세요.            |")
        print("+-------------------------------------------------+")
        post_idx = Utils.get_integer(10)

        selected_post = search_response[post_idx - 1]
        bookmark_id = self.bookmark_service.save(selected_post, user_id)

        print("+-------------------------------------------------+")
        print("|  북마크 등록을 완료했습니다.                    |")
        print("|  메모를 남기시겠습니까?                         |")
        print("+-------------------------------------------------+")
        print("|  1. Yes                                         |")
        print("|  2. No                                          |")
        print("+-------------------------------------------------+")
        memo_menu_iterator = Utils.get_integer(2)
        content = ""

        if memo_menu_iterator == 1:
            content = input(" > content: ")
            print("+-------------------------------------------------+")
            print("|                    저장 완료                    |")
            print("+-------------------------------------------------+")

        elif memo_menu_iterator == 2:
            content = ""

        self.memo_service.save(user_id, bookmark_id, content)

    @staticmethod
    def open_url(search_response):
        print("+-------------------------------------------------+")
        print("|  방문할 URL을 선택해주세요. (1~10)              |")
        print("+-------------------------------------------------+")
        url_idx = Utils.get_integer(10)
        opened_post = search_response[url_idx - 1]
        webbrowser.open_new(opened_post.link)

    def display_search_responses(self, bookmarks, search_response):
        for (idx, value) in enumerate(search_response):
            bookmark_count = 0

            for b in bookmarks:
                if b[0] == value.link:
                    bookmark_count = b[1]

            print(f"   {idx + 1}.")
            print("      제목 :", value.title)
            print("      미리보기 :", value.description)
            print("      링크 :", value.link)
            print("      날짜 :", self.format_date_string(value.postdate))
            print("      북마크 수 :", bookmark_count)
            print("      광고 여부 :", value.advertisement)
            print("      신뢰도 :", value.confidence)
            print()
