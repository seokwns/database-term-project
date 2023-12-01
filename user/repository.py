from .user import User


class UserRepository:

    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
        self.create()

    def create(self):
        # 유저 조회는 로그인 시에, 이메일을 이용하여 조회합니다.
        # 또한 중복 이메일 체크를 위해서도 이메일을 이용한 조회를 합니다.
        # 따라서 이메일에 인덱스를 추가합니다.

        # 이메일은 이메일 형식을 준수하도록 체크합니다.
        # 이름은 최소 2글자 입니다.
        # 비밀번호는 영문자, 숫자, 특수문자 포함 8글자 이상이어야 합니다.
        sql = '''
                CREATE TABLE IF NOT EXISTS user_tb (
                    id         SERIAL           PRIMARY KEY,
                    email      VARCHAR(100)     UNIQUE NOT NULL CHECK (email ~* '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'),
                    name       VARCHAR(10)      NOT NULL CHECK (LENGTH(name) >= 2 AND LENGTH(name) <= 10),
                    password   VARCHAR(30)      NOT NULL CHECK (password ~* '^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*]).{8,30}$'),
                    
                    INDEX idx_user_email (email)
                );
        '''

        self.cursor.execute(sql)
        self.connection.commit()

    def check_email_exists(self, email):
        sql = '''
                select count(*) 
                from user_tb u 
                where u.email like %s
        '''

        self.cursor.execute(sql, (f"%{email}%",))
        result = int(self.cursor.fetchone()[0])

        if result >= 1:
            return False

        return True

    def save_user(self, email, name, password):
        sql = '''
                insert into user_tb (email, name, password)
                values (%s, %s, %s)
        '''

        self.cursor.execute(sql, (f"{email}", f"{name}", f"{password}",))
        self.connection.commit()

    def find_user_by_email(self, email):
        sql = '''
                select *
                from user_tb u
                where u.email like %s
        '''

        self.cursor.execute(sql, (f"%{email}%",))
        record = self.cursor.fetchone()

        if record is None:
            return False

        return User(record)

    def delet_user(self, user_id):
        # 북마크 정보와 유저 정보를 삭제해야 합니다.
        # cascade 옵션이 있지만, 명시적으로 삭제를 진행합니다.
        # 두 테이블에서 삭제가 진행됩니다.
        # 따라서 오류 발생 시, 롤백을 해야 하므로 트랜잭션을 열어줍니다.
        sql = '''
                begin transaction isolation level repeatable read;
                
                delete from bookmark_tb
                where user_id = %s;
                
                delete from user_tb
                where id = %s;
                
                commit;
        '''

        self.cursor.execute(sql, (f'{user_id}', f'{user_id}', ))
        self.connection.commit()
