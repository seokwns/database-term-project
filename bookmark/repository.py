
class BookmarkRepository:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
        self.create()

    def create(self):
        sql = '''
                CREATE TABLE IF NOT EXISTS bookmark_tb (
                    id	        SERIAL          PRIMARY KEY,
                    url 	    VARCHAR(200)	NOT NULL,
                    title       VARCHAR(200)    NOT NULL,
                    user_id	    INTEGER      	NOT NULL,
                    
                    CONSTRAINT fk_user_bookmark
                        FOREIGN KEY (user_id)
                        REFERENCES user_tb (id)
                );
        '''

        self.cursor.execute(sql)
        self.connection.commit()

    def save(self, post, user_id):
        sql = '''
                insert into bookmark_tb (url, title, user_id)
                values (%s, %s, %s)
        '''

        url = post.link
        title = post.title
        self.cursor.execute(sql, (f'{url}', f'{title}', f'{user_id}', ))
        self.connection.commit()

    def find(self, user_id, page):
        sql = '''
                select *
                from bookmark_tb
                where user_id = %s
                limit 5
                offset %s
        '''

        self.cursor.execute(sql, (f'{user_id}', f'{page}', ))
        return self.connection.fetchall()
