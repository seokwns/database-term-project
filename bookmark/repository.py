
class BookmarkRepository:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
        self.create()

    def create(self):
        # 유저가 탈퇴하면 정보가 사라지고, 북마크 정보 또한 사라져야 합니다.
        # 따라서 cascade 옵션을 추가합니다.

        # 북마크는 중복되어 추가할 수 없습니다.
        # 따라서 유저와 url을 함께 unique 제약조건을 추가합니다.

        # 또한 북마크를 추가할 때는 유저 아이디 + url이며
        # 북마크 목록을 조회할 때는 유저 아이디만 가지고 조회하므로
        # user_id, url 순서로 인덱스를 추가합니다.
        sql = '''
                CREATE TABLE IF NOT EXISTS bookmark_tb (
                    id	        SERIAL          PRIMARY KEY,
                    url 	    VARCHAR(200)	NOT NULL,
                    title       VARCHAR(200)    NOT NULL,
                    user_id	    INTEGER      	NOT NULL,
                    
                    CONSTRAINT fk_user_bookmark
                        FOREIGN KEY (user_id)
                        REFERENCES user_tb (id)
                        ON DELETE CASCADE,
                        
                    CONSTRAINT uc_user_url 
                        UNIQUE (user_id, url),
                        
                    INDEX idx_user_id_url (user_id, url)
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
