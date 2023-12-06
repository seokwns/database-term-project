import psycopg2
import webbrowser
from user.service import UserService
from search.naver import search_keyword
from bookmark.service import BookmarkService
from memo.service import MemoService
from history.service import HistoryService


def format_date_string(input_string):
    if len(input_string) == 8:
        formatted_date = f'{input_string[:4]}-{input_string[4:6]}-{input_string[6:]}'
        return formatted_date
    else:
        return input_string


if __name__ == '__main__':
    connection = psycopg2.connect(
        database='sample2023',
        user='seokjun',
        password='qwer1234',
        host='::1',
        port='5432'
    )

    cursor = connection.cursor()

    user_service = UserService(connection, cursor)
    bookmark_service = BookmarkService(connection, cursor)
    memo_service = MemoService(connection, cursor)
    history_service = HistoryService(connection, cursor)

    user_id = -1

    while True:

        if user_id < 0:
            print("+-------------------------------------------------+")
            print("|                     mat-zip                     |")
            print("+-------------------------------------------------+")
            print("|  1. 회원가입                                    |")
            print("|  2. 로그인                                      |")
            print("|  3. 맛집 검색하기                               |")
            print("|  4. Exit                                        |")
            print("+-------------------------------------------------+")
        else:
            print("+-------------------------------------------------+")
            print("|                     mat-zip                     |")
            print("+-------------------------------------------------+")
            print("|  1. 로그아웃                                    |")
            print("|  2. 맛집 검색하기                               |")
            print("|  3. 북마크 목록                                 |")
            print("|  4. 검색 기록 보기                              |")
            print("|  5. 회원 탈퇴                                   |")
            print("|  6. Exit                                        |")
            print("+-------------------------------------------------+")

        itr = 0
        while True:
            try:
                itr = int(input(" > "))
                if user_id < 0:
                    if 1 <= itr <= 4:
                        break
                    else:
                        print("1~4 사이 숫자를 입력해주세요.")
                else:
                    if 1 <= itr <= 6:
                        break
                    else:
                        print("1~6 사이 숫자를 입력해주세요.")
            except ValueError:
                if user_id < 0:
                    print("1~4 사이 숫자를 입력해주세요.")
                else:
                    print("1~6 사이 숫자를 입력해주세요.")

        if user_id > 0 and itr == 1:
            user_id = -1
            print("로그아웃 완료")

        elif user_id < 0 and itr == 1:
            print("+---------------------------------------------------------------------------------+")
            print("|                                    회원가입                                     |")
            print("+---------------------------------------------------------------------------------+")
            print("|  회원가입 정보를 기입해주세요.                                                  |")
            print("|  - 이름은 2글자 이상, 10글자 이하만 가능합니다.                                 |")
            print("|  - 비밀번호는 영문자, 숫자, 특수문자 포함 8글자 이상, 30글자 이하만 가능합니다. |")
            print("+---------------------------------------------------------------------------------+")

            while True:
                email = input(" > email: ")
                name = input(" > name: ")
                password = input(" > password: ")

                registered = user_service.register(email, name, password)

                if registered is True:
                    break

            print("+--------------------------------------------------------------------------------+")
            print("|                                 회원가입 완료                                  |")
            print("+--------------------------------------------------------------------------------+")

        elif user_id < 0 and itr == 2:
            print("+-------------------------------------------------+")
            print("|                     로그인                      |")
            print("+-------------------------------------------------+")
            print("|  로그인 정보를 입력해주세요.                    |")
            print("+-------------------------------------------------+")
            email = input(" > email: ")
            password = input(" > password: ")

            user_id = user_service.login(email, password)

            if user_id > 0:
                print("+-------------------------------------------------+")
                print("|                   로그인 완료                   |")
                print("+-------------------------------------------------+")
            else:
                print("+-------------------------------------------------+")
                print("|                   로그인 실패                   |")
                print("+-------------------------------------------------+")
                print("|  비밀번호가 틀리거나 존재하지 않는 계정입니다.  |")
                print("+-------------------------------------------------+")

        elif (user_id < 0 and itr == 3) or (user_id > 0 and itr == 2):
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
                history_service.save(user_id, keyword, number)
                search_response = search_keyword(keyword, cursor, keyword, number)

                urls = []

                for response in search_response:
                    urls.append(response.link)

                bookmarks = bookmark_service.find_all_by_urls_in(urls)

                for (idx, value) in enumerate(search_response):
                    bookmark_count = 0

                    for b in bookmarks:
                        if b[0] == value.link:
                            bookmark_count = b[1]

                    print(f"   {idx + 1}.")
                    print("      제목 :", value.title)
                    print("      미리보기 :", value.description)
                    print("      링크 :", value.link)
                    print("      날짜 :", format_date_string(value.postdate))
                    print("      북마크 수 :", bookmark_count)
                    print("      광고 여부 :", value.advertisement)
                    print("      신뢰도 :", value.confidence)
                    print("+-------------------------------------------------+")

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
                    menu_iter = 0

                    while True:
                        try:
                            menu_iter = int(input(" > "))
                            if 1 <= menu_iter <= 5:
                                break
                            else:
                                print("+-------------------------------------------------+")
                                print("|  1~5 사이 숫자만 입력해주세요.                  |")
                                print("+-------------------------------------------------+")
                        except ValueError:
                            print("+-------------------------------------------------+")
                            print("|  1~5 사이 숫자만 입력해주세요.                  |")
                            print("+-------------------------------------------------+")

                    if menu_iter == 1:
                        number += 1
                        break

                    elif menu_iter == 2:
                        number -= 1
                        if number < 0:
                            number = 0
                        break

                    elif menu_iter == 3:
                        print("+-------------------------------------------------+")
                        print("|  방문할 URL을 선택해주세요.                     |")
                        print("+-------------------------------------------------+")

                        while True:
                            try:
                                url_idx = int(input(" > "))
                                if 1 <= url_idx <= 10:
                                    opened_post = search_response[url_idx - 1]
                                    webbrowser.open_new(opened_post.url)
                                    break
                                else:
                                    print("+-------------------------------------------------+")
                                    print("|  1~10 사이 숫자만 입력해주세요.                 |")
                                    print("+-------------------------------------------------+")
                            except ValueError:
                                print("+-------------------------------------------------+")
                                print("|  1~10 사이 숫자만 입력해주세요.                 |")
                                print("+-------------------------------------------------+")
                                continue

                    elif menu_iter == 4:
                        print("+-------------------------------------------------+")
                        print("|          포스트 번호를 입력해주세요.            |")
                        print("+-------------------------------------------------+")

                        post_idx = 0

                        while True:
                            try:
                                post_idx = int(input(" > "))
                                if 1 <= post_idx <= 10:
                                    break
                                else:
                                    print("+-------------------------------------------------+")
                                    print("|  1~10 사이 숫자만 입력해주세요.                 |")
                                    print("+-------------------------------------------------+")
                            except ValueError:
                                print("+-------------------------------------------------+")
                                print("|  1~10 사이 숫자만 입력해주세요.                 |")
                                print("+-------------------------------------------------+")

                        selected_post = search_response[post_idx - 1]
                        bookmark_id = bookmark_service.save(selected_post, user_id)

                        print("+-------------------------------------------------+")
                        print("|  북마크 등록을 완료했습니다.                    |")
                        print("|  메모를 남기시겠습니까?                         |")
                        print("+-------------------------------------------------+")
                        print("|  1. Yes                                         |")
                        print("|  2. No                                          |")
                        print("+-------------------------------------------------+")
                        memo_iter = int(input(" > "))

                        if memo_iter == 1:
                            content = input(" > content: ")
                            memo_service.save(user_id, bookmark_id, content)
                            print("+-------------------------------------------------+")
                            print("|                    저장 완료                    |")
                            print("+-------------------------------------------------+")

                    elif menu_iter == 5:
                        go_back = True
                        break

                if go_back is True:
                    break

        elif user_id > 0 and itr == 3:
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

                bookmark_iter = 0

                while True:
                    try:
                        bookmark_iter = int(input(" > "))
                        if 1 <= bookmark_iter <= 5:
                            break
                        else:
                            print("+-------------------------------------------------+")
                            print("|  1~5 사이 숫자만 입력해주세요.                  |")
                            print("+-------------------------------------------------+")
                    except ValueError:
                        print("+-------------------------------------------------+")
                        print("|  1~5 사이 숫자만 입력해주세요.                  |")
                        print("+-------------------------------------------------+")

                if bookmark_iter == 1 or bookmark_iter == 2:
                    page = 0
                    while True:
                        bookmarks = []
                        if bookmark_iter == 1:
                            bookmarks = bookmark_service.find(user_id, page)
                        elif bookmark_iter == 2:
                            bookmarks = bookmark_service.find_order_by_date(user_id, page)

                        if len(bookmarks) == 0:
                            print("+-------------------------------------------------+")
                            print("|  북마크가 존재하지 않습니다.                    |")
                            print("+-------------------------------------------------+")
                            break

                        for (idx, value) in enumerate(bookmarks):
                            print("+-------------------------------------------------+")
                            print(f'{idx + 1}.')
                            print("   url :", value.url)
                            print("   title :", value.title)
                            print("   content :", value.memo_content)
                            print("   created at :", value.memo_created_at)
                            print("+-------------------------------------------------+")

                        print("+-------------------------------------------------+")
                        print("|                   북마크 메뉴                   |")
                        print("+-------------------------------------------------+")
                        print("|  1. 다음 페이지 보기                            |")
                        print("|  2. 이전 페이지 보기                            |")
                        print("|  3. 북마크 삭제하기                             |")
                        print("|  4. 메모 추가/수정하기                          |")
                        print("|  5. 뒤로가기                                    |")
                        print("+-------------------------------------------------+")
                        menu_iter = int(input(" > "))

                        if menu_iter == 1:
                            page += 1
                            continue

                        elif menu_iter == 2:
                            page -= 1
                            if page < 0:
                                page = 0
                            continue

                        elif menu_iter == 3:
                            print("+-------------------------------------------------+")
                            print("|  삭제할 북마크 번호를 입력해주세요. (1~10)      |")
                            print("|  취소할 경우 0을 입력해주세요.                  |")
                            print("+-------------------------------------------------+")
                            bookmark_idx = 0

                            while True:
                                try:
                                    bookmark_idx = int(input(" > "))
                                    if 0 <= bookmark_idx <= 10:
                                        break
                                    else:
                                        print("+-------------------------------------------------+")
                                        print("|  1 ~ 10 사이 숫자만 입력해주세요.               |")
                                        print("+-------------------------------------------------+")
                                except ValueError:
                                    print("+-------------------------------------------------+")
                                    print("|  1 ~ 10 사이 숫자만 입력해주세요.               |")
                                    print("+-------------------------------------------------+")

                            if bookmark_idx == 0:
                                continue

                            selected_bookmark = bookmarks[bookmark_idx - 1]
                            bookmark_url = selected_bookmark.url
                            bookmark_service.delete(user_id, bookmark_url)

                        elif menu_iter == 4:
                            print("+-------------------------------------------------+")
                            print("|  수정할 북마크 번호를 입력해주세요. (1~10)      |")
                            print("|  취소할 경우 0을 입력해주세요.                  |")
                            print("+-------------------------------------------------+")
                            while True:
                                try:
                                    selected_memo_idx = int(input(" > "))
                                    if 0 <= selected_memo_idx <= 10:
                                        break
                                    else:
                                        print("+-------------------------------------------------+")
                                        print("|  1 ~ 10 사이 숫자만 입력해주세요.               |")
                                        print("+-------------------------------------------------+")
                                except ValueError:
                                    print("+-------------------------------------------------+")
                                    print("|  1 ~ 10 사이 숫자만 입력해주세요.               |")
                                    print("+-------------------------------------------------+")

                            if selected_memo_idx == 0:
                                break

                            selected_memo = bookmarks[selected_memo_idx - 1]

                            print("기존 내용")
                            print(selected_memo.memo_content)
                            print("+-------------------------------------------------+")
                            print("수정 후 내용")
                            updated_content = input(" > ")

                            memo_service.update(user_id, selected_memo.url, updated_content)
                            print("+-------------------------------------------------+")
                            print("|                    저장 완료                    |")
                            print("+-------------------------------------------------+")

                        elif menu_iter == 5:
                            break

                elif bookmark_iter == 3 or bookmark_iter == 4:
                    keyword = input(" > keyword: ")
                    responses = []

                    if bookmark_iter == 3:
                        responses = bookmark_service.find_in_title(user_id, keyword)

                        if len(responses) == 0:
                            print("+----------------------------------------------------+")
                            print("|  해당 키워드가 포함된 북마크가 존재하지 않습니다.  |")
                            print("+----------------------------------------------------+")
                            continue

                    elif bookmark_iter == 4:
                        responses = bookmark_service.find_in_title_and_memo(user_id, keyword)

                        if len(responses) == 0:
                            print("+--------------------------------------------------------------+")
                            print("|  해당 키워드가 포함된 북마크 혹은 메모가 존재하지 않습니다.  |")
                            print("+--------------------------------------------------------------+")
                            continue

                    for (idx, value) in enumerate(responses):
                        print("+--------------------------------------------------------------+")
                        print(f'   {idx + 1}.')
                        print("      url :", value.url)
                        print("      title :", value.title)
                        print("      content :", value.memo_content)
                        print("      created at :", value.memo_created_at)
                        print("+--------------------------------------------------------------+")

                elif bookmark_iter == 5:
                    break

        elif user_id > 0 and itr == 4:
            page = 0
            while True:
                print("+-------------------------------------------------+")
                print("|                  검색기록 메뉴                  |")
                print("+-------------------------------------------------+")
                print("|  1. 기록 보기                                   |")
                print("|  2. 키워드로 검색하기                           |")
                print("|  3. 뒤로가기                                    |")
                print("+-------------------------------------------------+")

                history_menu_iter = 1
                while True:
                    try:
                        history_menu_iter = int(input(" > "))
                        if 1 <= history_menu_iter <= 4:
                            break
                        else:
                            print("+-------------------------------------------------+")
                            print("|  1~4 사이 숫자만 입력해주세요.                  |")
                            print("+-------------------------------------------------+")
                    except ValueError:
                        print("+-------------------------------------------------+")
                        print("|  1~4 사이 숫자만 입력해주세요.                  |")
                        print("+-------------------------------------------------+")
                        continue

                if history_menu_iter == 1 or history_menu_iter == 2:
                    page = 0
                    while True:
                        histories = []

                        if history_menu_iter == 1:
                            histories = history_service.find_by_user_id(user_id, page)
                        elif history_menu_iter == 2:
                            history_keyword = input(" > keyword : ")
                            print("+--------------------------------------------------------------+")
                            histories = history_service.find_by_user_id_and_keyword(user_id, history_keyword, page)

                        for (idx, value) in enumerate(histories):
                            print(f'   {idx + 1}.')
                            print("      키워드 =", value.keyword)
                            print("      페이지 =", value.page)
                            print("      날짜 =", value.searched_at)
                            print("+--------------------------------------------------------------+")

                        print("+-------------------------------------------------+")
                        print("|                  검색기록 메뉴                  |")
                        print("+-------------------------------------------------+")
                        print("|  1. 다음 페이지 보기                            |")
                        print("|  2. 이전 페이지 보기                            |")
                        print("|  3. 뒤로가기                                    |")
                        print("+-------------------------------------------------+")

                        history_menu_iter2 = 0
                        while True:
                            try:
                                history_menu_iter2 = int(input(" > "))
                                if 1 <= history_menu_iter2 <= 3:
                                    break
                                else:
                                    print("+-------------------------------------------------+")
                                    print("|  1~3 사이 숫자만 입력해주세요.                  |")
                                    print("+-------------------------------------------------+")
                            except ValueError:
                                print("+-------------------------------------------------+")
                                print("|  1~3 사이 숫자만 입력해주세요.                  |")
                                print("+-------------------------------------------------+")
                                continue

                        if history_menu_iter2 == 1:
                            page += 1
                        elif history_menu_iter2 == 2:
                            page -= 1
                            if page < 0:
                                page = 0
                        elif history_menu_iter2 == 3:
                            break

                elif history_menu_iter == 3:
                    break

        elif user_id > 0 and itr == 5:
            print("+-------------------------------------------------+")
            print("|                    회원 탈퇴                    |")
            print("+-------------------------------------------------+")
            print("|  1. Yes                                         |")
            print("|  2. No                                          |")
            print("+-------------------------------------------------+")
            delete_iter = int(input(" > "))

            if delete_iter == 1:
                user_service.delete(user_id)
                user_id = -1
                print("+-------------------------------------------------+")
                print("|                    탈퇴 완료                    |")
                print("+-------------------------------------------------+")

        elif (user_id < 0 and itr == 4) or (user_id > 0 and itr == 6):
            print("+-------------------------------------------------+")
            print("|                       Bye                       |")
            print("+-------------------------------------------------+")
            break

    cursor.close()
    connection.close()
