import math

from utils import Utils


class BookmarkController:
    def __init__(self, connection, cursor, bookmark_service, memo_service):
        self.connection = connection
        self.cursor = cursor
        self.bookmark_service = bookmark_service
        self.memo_service = memo_service

    def find_bookmarks(self, user_id, bookmark_iter):
        page = 0
        max_page = 0
        keyword = ""

        if bookmark_iter == 3 or bookmark_iter == 4:
            keyword = input(" > keyword: ")

        while True:
            bookmarks = []
            bookmark_count = 0

            if bookmark_iter == 1:
                bookmarks, bookmark_count = self.bookmark_service.find(user_id, page)

            elif bookmark_iter == 2:
                bookmarks, bookmark_count = self.bookmark_service.find_order_by_date(user_id, page)

            elif bookmark_iter == 3:
                bookmarks, bookmark_count = self.bookmark_service.find_in_title(user_id, keyword)

                if len(bookmarks) == 0:
                    print("+----------------------------------------------------+")
                    print("|  해당 키워드가 포함된 북마크가 존재하지 않습니다.  |")
                    print("+----------------------------------------------------+")
                    return

            elif bookmark_iter == 4:
                bookmarks, bookmark_count = self.bookmark_service.find_in_title_and_memo(user_id, keyword)

                if len(bookmarks) == 0:
                    print("+--------------------------------------------------------------+")
                    print("|  해당 키워드가 포함된 북마크 혹은 메모가 존재하지 않습니다.  |")
                    print("+--------------------------------------------------------------+")
                    return

            max_page = math.ceil(bookmark_count / 10)

            if len(bookmarks) == 0:
                print("+-------------------------------------------------+")
                print("|  북마크가 존재하지 않습니다.                    |")
                print("+-------------------------------------------------+")
                break

            for (idx, value) in enumerate(bookmarks):
                print(f'{idx + 1}.')
                print("   url :", value.url)
                print("   title :", value.title)
                print("   content :", value.memo_content)
                print("   created at :", value.memo_created_at)

            print("+-------------------------------------------------+")
            print("|                   북마크 메뉴                   |")
            print("+-------------------------------------------------+")
            print("|  1. 다음 페이지 보기                            |")
            print("|  2. 이전 페이지 보기                            |")
            print("|  3. 북마크 삭제하기                             |")
            print("|  4. 메모 추가/수정하기                          |")
            print("|  5. 뒤로가기                                    |")
            print("+-------------------------------------------------+")
            menu_iter = Utils.get_integer(5)

            if menu_iter == 1:
                page += 1
                if page > max_page:
                    print("+-------------------------------------------------+")
                    print("|  마지막 페이지 입니다.                          |")
                    print("+-------------------------------------------------+")
                    page -= 1
                continue

            elif menu_iter == 2:
                page -= 1
                if page < 0:
                    print("+-------------------------------------------------+")
                    print("|  첫번쨰 페이지 입니다.                          |")
                    print("+-------------------------------------------------+")
                    page = 0
                continue

            elif menu_iter == 3:
                print("+-------------------------------------------------+")
                print(f"|  삭제할 북마크 번호를 입력해주세요. (1~{len(bookmarks)})      |")
                print("|  취소할 경우 0을 입력해주세요.                  |")
                print("+-------------------------------------------------+")
                bookmark_idx = Utils.get_integer(len(bookmarks), 0)

                if bookmark_idx == 0:
                    continue

                selected_bookmark = bookmarks[bookmark_idx - 1]
                bookmark_url = selected_bookmark.url
                self.bookmark_service.delete(user_id, bookmark_url)

            elif menu_iter == 4:
                print("+-------------------------------------------------+")
                print(f"|  수정할 북마크 번호를 입력해주세요. (1~{len(bookmarks):2d})      |")
                print("|  취소할 경우 0을 입력해주세요.                  |")
                print("+-------------------------------------------------+")
                selected_memo_idx = Utils.get_integer(len(bookmarks), 0)

                if selected_memo_idx == 0:
                    break

                selected_memo = bookmarks[selected_memo_idx - 1]

                print("기존 내용")
                print(selected_memo.memo_content)
                print("+-------------------------------------------------+")
                print("수정 후 내용")
                updated_content = input(" > ")

                self.memo_service.update(user_id, selected_memo.url, updated_content)
                print("+-------------------------------------------------+")
                print("|                    저장 완료                    |")
                print("+-------------------------------------------------+")

            elif menu_iter == 5:
                break
