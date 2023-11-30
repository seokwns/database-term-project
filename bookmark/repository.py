
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
                    user_id	    INTEGR      	NOT NULL,
                    
                    CONSTRAINT fk_user_bookmark
                        FOREIGN KEY (user_id)
                        REFERENCES user_tb (id)
                );
        '''

        self.cursor.execute(sql)
        self.connection.commit()
