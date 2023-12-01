import psycopg2
from user.service import UserService
from search.naver import search_keyword
from bookmark.service import BookmarkService

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

    user_id = -1

    while True:
        print()
        print("------------------------------")
        print()
        print("mat-zip")
        print("1. 회원가입")
        print("2. 로그인")
        print("3. 맛집 검색하기")
        print("4. 북마크 목록 보기")
        print("5. Exit")
        print()
        print("------------------------------")
        print()

        itr = int(input(" > "))

        if itr == 1:
            print()
            print("------------------------------")
            print()
            print("[ 회원가입 ]")
            print()
            print("회원가입 정보를 기입해주세요.")
            print("- 이름은 2글자 이상, 10글자 이하만 가능합니다.")
            print("- 비밀번호는 영문자, 숫자, 특수문자 포함 8글자 이상, 30글자 이하만 가능합니다.")
            print()
            print("------------------------------")
            print()

            while True:
                email = input(" > email: ")
                name = input(" > name: ")
                password = input(" > password: ")

                registered = user_service.register(email, name, password)

                if registered is True:
                    break

            print()
            print("------------------------------")
            print()
            print("[ 회원가입 ]")
            print()
            print("회원가입 완료!")
            print()
            print("------------------------------")
            print()

        elif itr == 2:
            print()
            print("------------------------------")
            print()
            print("[ 로그인 ]")
            print()
            print("로그인 정보를 입력해주세요.")
            print()
            print("------------------------------")
            print()

            email = input(" > email: ")
            password = input(" > password: ")

            user_id = user_service.login(email, password)

            if user_id > 0:
                print()
                print("------------------------------")
                print()
                print("[ 로그인 완료 ]")
                print()
                print("------------------------------")
                print()
            else:
                print()
                print("------------------------------")
                print()
                print("[ 로그인 실패 ]")
                print()
                print("비밀번호가 틀렸거나 존재하지 않는 계정입니다.")
                print()
                print("------------------------------")
                print()

        elif itr == 3:
            print()
            print("------------------------------")
            print()
            print("[ 맛집 검색하기 ]")
            print()
            print("키워드를 입력해주세요!")
            print()
            print("------------------------------")
            print()

            keyword = input(" > keyword: ")
            number = int(input(" > 페이지: "))

            while True:
                print("검색 중입니다. 잠시만 기다려 주세요 .....")
                search_response = search_keyword(keyword, cursor, keyword, number)
                for (idx, value) in enumerate(search_response):
                    print()
                    print(f"{idx + 1}.")
                    print("title :", value.title)
                    print("description :", value.description)
                    print("link :", value.link)
                    print("date :", value.postdate)
                    print("advertisement :", value.advertisement)
                    print("confidence :", value.confidence)
                    print()

                go_back = False

                while True:
                    print()
                    print("[ 검색 메뉴 ]")
                    print()
                    print("1. 다음 페이지 보기")
                    print("2. 북마크 추가하기")
                    print("3. 메인 메뉴로 돌아가기")
                    print()
                    menu_iter = int(input(" > "))

                    if menu_iter == 1:
                        number += 1
                        break
                    elif menu_iter == 2:
                        print("포스트 번호를 입력해주세요. (1~10)")

                        while True:
                            post_idx = int(input(" > "))

                            if 1 <= post_idx <= 10:
                                selected_post = search_response[post_idx - 1]
                                bookmark_service.save(selected_post, user_id)
                                print("북마크 등록을 완료했습니다.")
                                break
                            else:
                                print("1 ~ 10 사이의 번호를 입력해주세요.")
                    elif menu_iter == 3:
                        go_back = True
                        break
                    else:
                        print("1 ~ 3 사이의 번호를 입력해주세요.")

                if go_back is True:
                    break

        elif itr == 4:
            if user_id < 1:
                print("로그인 후 이용 가능합니다.")
                print("로그인을 해주세요")
                continue

            print()
            print("------------------------------")
            print()
            print("[ 북마크 목록 보기 ] ")
            print()
            print("------------------------------")
            print()

            page = 1
            while True:
                bookmarks = bookmark_service.find(user_id, page)
                for (idx, value) in enumerate(bookmarks):
                    print()
                    print(f'{idx + 1}.')
                    print("url :", value.url)
                    print("title :", value.title)
                    print()

                print()
                print("[ 북마크 메뉴 ]")
                print()
                print("1. 다음 페이지 보기")
                print("2. 북마크 삭제하기")
                print("3. 메인 메뉴로 돌아가기")
                print()

                menu_iter = int(input(" > "))

                if menu_iter == 1:
                    page = 2
                    continue
                elif menu_iter == 2:
                    print("삭제할 북마크 번호를 입력해주세요. (1~10")
                    bookmark_idx = int(input(" > "))

                elif menu_iter == 3:
                    break

        elif itr == 5:
            print()
            print("------------------------------")
            print()
            print("[ Bye ]")
            print()
            print("------------------------------")
            print()
            break

    cursor.close()
    connection.close()
