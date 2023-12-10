class HistoryRepository:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
        self.create()

    def create(self):
        sql = '''
                CREATE TABLE IF NOT EXISTS history_tb (
                    id              SERIAL          PRIMARY KEY,
                    user_id         INT             NOT NULL,
                    keyword         VARCHAR(255),
                    page            INTEGER,
                    searched_at     TIMESTAMP       NOT NULL,
                                        
                    CONSTRAINT fk_user_history
                        FOREIGN KEY (user_id)
                        REFERENCES user_tb (id)
                        ON DELETE CASCADE,
                        
                    CONSTRAINT unique_user_history
                        UNIQUE (user_id, keyword, page, searched_at)
                );
                
                CREATE INDEX ON history_tb (user_id);
        '''

        self.cursor.execute(sql)
        self.connection.commit()

    def save(self, user_id, keyword, page):
        sql = '''
                insert into history_tb (user_id, keyword, page, searched_at)
                values (%s, %s, %s, CURRENT_TIMESTAMP)
        '''

        self.cursor.execute(sql, (user_id, keyword, page))
        self.connection.commit()

    def find_by_user_id(self, user_id, page):
        sql = '''
                select *
                from history_tb h
                where h.user_id = %s
                order by searched_at desc
                limit 10
                offset %s
        '''

        self.cursor.execute(sql, (user_id, page * 10, ))
        responses = self.cursor.fetchall()

        sql = '''
                select count(*)
                from history_tb
                where user_id = %s
        '''

        self.cursor.execute(sql, (user_id, ))
        count = self.cursor.fetchone()

        return responses, count

    def find_by_user_id_and_keyword(self, user_id, keyword, page):
        sql = '''
                select *
                from history_tb
                where user_id = %s and keyword like %s
                order by searched_at desc
                limit 10
                offset %s
        '''

        self.cursor.execute(sql, (user_id, f'%{keyword}%', page * 10, ))
        responses = self.cursor.fetchall()

        sql = '''
                select count(*)
                from history_tb 
                where user_id = %s and keyword like %s
        '''

        self.cursor.execute(sql, (user_id, keyword, ))
        count = self.cursor.fetchone()

        return responses, count
