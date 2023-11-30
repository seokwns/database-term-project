from .user import User


class UserRepository:

    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
        self.create()

    def create(self):
        sql = '''
                CREATE TABLE IF NOT EXISTS user_tb (
                    id         SERIAL           PRIMARY KEY,
                    email      VARCHAR(100)     UNIQUE NOT NULL,
                    name       VARCHAR(10)      NOT NULL,
                    password   VARCHAR(30)      NOT NULL
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

        print("user = ", record)

        if record is None:
            return False

        return User(record)
