import psycopg2
from user.service import UserService
from search.naver import search_keyword
from bookmark.service import BookmarkService
from memo.service import MemoService


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

    user_id = -1

    while True:

        if user_id < 0:
            print("------------------------------")
            print("mat-zip")
            print("1. 회원가입")
            print("2. 로그인")
            print("3. 맛집 검색하기")
            print("4. Exit")
            print("------------------------------")
        else:
            print("------------------------------")
            print("mat-zip")
            print("1. 로그아웃")
            print("2. 맛집 검색하기")
            print("3. 북마크 목록")
            print("4. 회원 탈퇴")
            print("5. Exit")
            print("------------------------------")

        itr = int(input(" > "))

        if user_id > 0 and itr == 1:
            user_id = -1
            print("로그아웃 완료")

        elif user_id < 0 and itr == 1:
            print("------------------------------")
            print("[ 회원가입 ]")
            print()
            print("회원가입 정보를 기입해주세요.")
            print("- 이름은 2글자 이상, 10글자 이하만 가능합니다.")
            print("- 비밀번호는 영문자, 숫자, 특수문자 포함 8글자 이상, 30글자 이하만 가능합니다.")
            print("------------------------------")

            while True:
                email = input(" > email: ")
                name = input(" > name: ")
                password = input(" > password: ")

                registered = user_service.register(email, name, password)

                if registered is True:
                    break

            print("------------------------------")
            print("회원가입 완료!")
            print("------------------------------")

        elif user_id < 0 and itr == 2:
            print("------------------------------")
            print("[ 로그인 ]")
            print()
            print("로그인 정보를 입력해주세요.")
            print("------------------------------")
            email = input(" > email: ")
            password = input(" > password: ")

            user_id = user_service.login(email, password)

            if user_id > 0:
                print("------------------------------")
                print("[ 로그인 완료 ]")
                print("------------------------------")
            else:
                print("------------------------------")
                print("[ 로그인 실패 ]")
                print()
                print("비밀번호가 틀렸거나 존재하지 않는 계정입니다.")
                print("------------------------------")

        elif (user_id < 0 and itr == 3) or (user_id > 0 and itr == 2):
            print("------------------------------")
            print("[ 맛집 검색하기 ]")
            print()
            print("키워드를 입력해주세요!")
            print("------------------------------")
            keyword = input(" > keyword: ")
            number = int(input(" > 페이지: "))

            if number < 1:
                number = 1

            while True:
                print("검색 중입니다. 잠시만 기다려 주세요 .....")
                print()
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

                    print(f"{idx + 1}.")
                    print("제목 :", value.title)
                    print("미리보기 :", value.description)
                    print("링크 :", value.link)
                    print("날짜 :", format_date_string(value.postdate))
                    print("북마크 수 :", bookmark_count)
                    print("광고 여부 :", value.advertisement)
                    print("신뢰도 :", value.confidence)
                    print()

                go_back = False

                while True:
                    print("[ 검색 메뉴 ]")
                    print()
                    print("1. 다음 페이지 보기")
                    print("2. 이전 페이지 보기")
                    print("3. 북마크 추가하기")
                    print("4. 메인 메뉴로 돌아가기")
                    menu_iter = int(input(" > "))

                    if menu_iter == 1:
                        number += 1
                        break

                    elif menu_iter == 2:
                        number -= 1
                        if number < 0:
                            number = 0
                        break

                    elif menu_iter == 3:
                        if user_id < 0:
                            print("로그인 후 이용 가능합니다.")
                            continue

                        print("포스트 번호를 입력해주세요. (1~10)")

                        while True:
                            post_idx = int(input(" > "))

                            if 1 <= post_idx <= 10:
                                selected_post = search_response[post_idx - 1]
                                bookmark_id = bookmark_service.save(selected_post, user_id)
                                print("북마크 등록을 완료했습니다.")
                                print("메모를 남기시겠습니까?")
                                print("1. Yes")
                                print("2. No")
                                memo_iter = int(input(" > "))

                                if memo_iter == 1:
                                    content = input(" > content: ")
                                    memo_service.save(user_id, bookmark_id, content)
                                    print()
                                    print("저장 완료")
                                    print()

                                break

                            else:
                                print("1 ~ 10 사이의 번호를 입력해주세요.")

                    elif menu_iter == 4:
                        go_back = True
                        break

                    else:
                        print("1 ~ 4 사이의 번호를 입력해주세요.")

                if go_back is True:
                    break

        elif user_id > 0 and itr == 3:
            if user_id < 1:
                print("로그인 후 이용 가능합니다.")
                print("로그인을 해주세요")
                continue

            while True:
                print("------------------------------")
                print("[ 북마크 목록 ] ")
                print()
                print("1. 목록 보기")
                print("2. 최근에 추가한 순서로 보기")
                print("3. 제목에서 검색하기")
                print("4. 제목과 메모에서 검색하기")
                print("5. 메뉴로 돌아가기")
                print("------------------------------")

                bookmark_iter = int(input(" > "))

                if bookmark_iter == 1 or bookmark_iter == 2:
                    page = 0
                    while True:
                        bookmarks = []
                        if bookmark_iter == 1:
                            bookmarks = bookmark_service.find(user_id, page)
                        elif bookmark_iter == 2:
                            bookmarks = bookmark_service.find_order_by_date(user_id, page)

                        if len(bookmarks) == 0:
                            print("북마크가 존재하지 않습니다.")
                            break

                        for (idx, value) in enumerate(bookmarks):
                            print(f'{idx + 1}.')
                            print("url :", value.url)
                            print("title :", value.title)
                            print("content :", value.memo_content)
                            print("created at :", value.memo_created_at)
                            print()

                        print("[ 북마크 메뉴 ]")
                        print()
                        print("1. 다음 페이지 보기")
                        print("2. 이전 페이지 보기")
                        print("3. 북마크 삭제하기")
                        print("4. 메모 수정하기")
                        print("5. 메인 메뉴로 돌아가기")
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
                            print("삭제할 북마크 번호를 입력해주세요. (1~10)")
                            print("취소할 경우 0을 입력해주세요.")
                            while True:
                                bookmark_idx = int(input(" > "))

                                if 1 <= bookmark_idx <= 10:
                                    bookmark_url = bookmarks[bookmark_idx - 1].url
                                    bookmark_service.delete(user_id, bookmark_url)
                                    break

                                elif bookmark_idx == 0:
                                    break

                                else:
                                    print("1 ~ 10 사이의 번호를 입력해주세요.")

                        elif menu_iter == 4:
                            print("수정할 북마크를 입력해주세요. (1~10)")
                            print("취소할 경우 0을 입력해주세요.")
                            while True:
                                selected_memo_idx = int(input(" > "))

                                if 1 <= selected_memo_idx <= 10:
                                    selected_memo = bookmarks[selected_memo_idx - 1]

                                    print("기존 내용 ")
                                    print(selected_memo.memo_content)
                                    print()
                                    print("수정 후 내용")
                                    updated_content = input(" > ")

                                    memo_service.update(user_id, selected_memo.url, updated_content)
                                    break

                                elif selected_memo_idx == 0:
                                    break

                                else:
                                    print("1 ~ 10 사이의 번호를 입력해주세요.")

                        elif menu_iter == 5:
                            break

                elif bookmark_iter == 3 or bookmark_iter == 4:
                    keyword = input(" > keyword: ")
                    responses = []

                    if bookmark_iter == 3:
                        responses = bookmark_service.find_in_title(user_id, keyword)
                    elif bookmark_iter == 4:
                        responses = bookmark_service.find_in_title_and_memo(user_id, keyword)

                    if len(responses) == 0:
                        print("북마크 목록이 존재하지 않습니다.")
                        break

                    for (idx, value) in enumerate(responses):
                        print()
                        print(f'{idx + 1}.')
                        print("url :", value.url)
                        print("title :", value.title)
                        print("content :", value.memo_content)
                        print("created at :", value.memo_created_at)

                elif bookmark_iter == 5:
                    break

        elif user_id > 0 and itr == 4:
            print("회원 탈퇴를 진행하시겠습니까?")
            print("1. Yes")
            print("2. No")
            delete_iter = int(input(" > "))

            if delete_iter == 1:
                user_service.delete(user_id)
                user_id = -1
                print("탈퇴 완료")

        elif (user_id < 0 and itr == 4) or (user_id > 0 and itr == 5):
            print("------------------------------")
            print()
            print("[ Bye ]")
            print()
            print("------------------------------")
            break

    cursor.close()
    connection.close()
