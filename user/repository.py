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
                    email      VARCHAR(100)     UNIQUE NOT NULL CHECK (email ~* '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'),
                    name       VARCHAR(10)      NOT NULL CHECK (LENGTH(name) >= 2 AND LENGTH(name) <= 10),
                    password   VARCHAR(30)      NOT NULL CHECK (password ~* '^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*]).{8,30}$')
                );
                
                CREATE INDEX ON user_tb (email);
        '''

        self.cursor.execute(sql)
        self.connection.commit()

    def check_email_exists(self, email):
        sql = '''
                select count(*) 
                from user_tb u 
                where u.email like %s
        '''

        self.cursor.execute(sql, (email, ))
        result = int(self.cursor.fetchone()[0])

        if result >= 1:
            return False

        return True

    def save_user(self, email, name, password):
        sql = '''
                insert into user_tb (email, name, password)
                values (%s, %s, %s)
        '''

        self.cursor.execute(sql, (email, name, password, ))
        self.connection.commit()

    def find_user_by_email(self, email):
        sql = '''
                select *
                from user_tb u
                where u.email like %s
        '''

        self.cursor.execute(sql, (email, ))
        record = self.cursor.fetchone()

        if record is None:
            return False

        return User(record)

    def delete_user(self, user_id):
        try:
            self.connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)

            sql = '''
                    begin;
                    
                    with bookmark_ids as (
                        select b.id
                        from bookmark_tb b
                        where b.user_id = %s
                    )
                    delete from memo_tb m
                    where m.bookmark_id in (select id from bookmark_ids);
                    
                    delete from bookmark_tb
                    where user_id = %s;
                    
                    delete from history_tb
                    where user_id = %s;
                    
                    delete from user_tb
                    where id = %s;
                    
                    commit;
            '''

            self.cursor.execute(sql, (user_id, user_id, user_id, user_id, ))
            self.connection.commit()

        except Exception as e:
            self.connection.rollback()
            raise e
