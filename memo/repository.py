class MemoRepository:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
        self.create()

    def create(self):
        sql = '''
                CREATE TABLE IF NOT EXISTS memo_tb (
                    id          SERIAL          PRIMARY KEY,
                    user_id     INTEGER         NOT NULL,
                    bookmark_id INTEGER NOT     NULL,
                    content     VARCHAR(500)    NOT NULL,
                    created_at  TIMESTAMP       NOT NULL,
                    
                    CONSTRAINT fk_memo_bookmark
                        FOREIGN KEY (bookmark_id)
                        REFERENCES bookmark_tb (id)
                        ON DELETE CASCADE,
                    
                    CONSTRAINT fk_memo_user
                        FOREIGN KEY (user_id)
                        REFERENCES user_tb (id)
                        ON DELETE CASCADE
                );
                
                CREATE INDEX ON memo_tb (user_id, bookmark_id);
        '''

        self.cursor.execute(sql)
        self.connection.commit()

    def save(self, user_id, bookmark_id, content):
        sql = '''
                insert into memo_tb (user_id, bookmark_id, content, created_at) 
                values (%s, %s, %s, CURRENT_TIMESTAMP)
        '''

        self.cursor.execute(sql, (user_id, bookmark_id, content, ))
        self.connection.commit()

    def update(self, user_id, url, content):
        sql = '''
                update memo_tb
                set content = %s
                where user_id = %s and bookmark_id = (
                    select id
                    from bookmark_tb
                    where user_id = %s and url = %s
                );
        '''

        self.cursor.execute(sql, (content, user_id, user_id, url, ))
        self.connection.commit()
