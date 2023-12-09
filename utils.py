class Utils:
    @staticmethod
    def get_integer(max_number, min_number=1):
        while True:
            try:
                menu_iter = int(input(" > "))
                if min_number <= menu_iter <= max_number:
                    break
                else:
                    print("+-------------------------------------------------+")
                    print(f"|  {min_number}~{' ' if max_number < 10 else ''}{max_number} 사이 숫자만 입력해주세요.                 |")
                    print("+-------------------------------------------------+")
            except ValueError:
                print("+-------------------------------------------------+")
                print(f"|  {min_number}~{' ' if max_number < 10 else ''}{max_number} 사이 숫자만 입력해주세요.                 |")
                print("+-------------------------------------------------+")
                continue

        return menu_iter

    @staticmethod
    def get_main_menu_iterator(user_id):
        while True:
            try:
                menu_iter = int(input(" > "))
                if user_id < 0:
                    if 1 <= menu_iter <= 4:
                        break
                    else:
                        print("+-------------------------------------------------+")
                        print("|  1~4 사이 숫자를 입력해주세요.                  |")
                        print("+-------------------------------------------------+")
                else:
                    if 1 <= menu_iter <= 6:
                        break
                    else:
                        print("+-------------------------------------------------+")
                        print("|  1~6 사이 숫자를 입력해주세요.                  |")
                        print("+-------------------------------------------------+")
            except ValueError:
                if user_id < 0:
                    print("+-------------------------------------------------+")
                    print("|  1~4 사이 숫자를 입력해주세요.                  |")
                    print("+-------------------------------------------------+")
                else:
                    print("+-------------------------------------------------+")
                    print("|  1~6 사이 숫자를 입력해주세요.                  |")
                    print("+-------------------------------------------------+")

        return menu_iter
