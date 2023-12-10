import psycopg2.extensions


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
                    created_at  TIMESTAMP       NOT NULL,
                    
                    CONSTRAINT fk_user_bookmark
                        FOREIGN KEY (user_id)
                        REFERENCES user_tb (id)
                        ON DELETE CASCADE,
                        
                    CONSTRAINT uc_user_url 
                        UNIQUE (user_id, url)
                );
                
                CREATE INDEX ON bookmark_tb (user_id, url);
                CREATE INDEX ON bookmark_tb (url);
        '''

        self.cursor.execute(sql)
        self.connection.commit()

    def save(self, post, user_id):
        sql = '''
                insert into bookmark_tb (url, title, user_id, created_at)
                values (%s, %s, %s, CURRENT_TIMESTAMP)
        '''

        url = post.link
        title = post.title
        self.cursor.execute(sql, (url, title, user_id, ))
        self.connection.commit()

        sql = '''
                select b.id
                from bookmark_tb b
                where user_id = %s and url = %s
        '''

        self.cursor.execute(sql, (user_id, url, ))
        return self.cursor.fetchone()

    def find(self, user_id, page):
        sql = '''
                select *
                from bookmark_tb b
                left outer join memo_tb m on b.id = m.bookmark_id
                where b.user_id = %s
                limit 10
                offset %s
        '''

        self.cursor.execute(sql, (user_id, page * 10, ))
        responses = self.cursor.fetchall()

        sql = '''
                select count(*)
                from bookmark_tb
                where user_id = %s        
        '''

        self.cursor.execute(sql, (user_id, ))
        bookmark_count = self.cursor.fetchone()

        return responses, bookmark_count

    def find_all_by_urls_in(self, urls):
        url_str = ','.join(map(lambda x: f"'{x}'", urls))

        sql = f'''
                select url, count(url)
                from bookmark_tb
                where url in ({url_str})
                group by url
        '''

        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def find_order_by_date(self, user_id, page):
        sql = '''
                select *
                from bookmark_tb b
                left outer join memo_tb m on b.id = m.bookmark_id
                where b.user_id = %s
                order by b.created_at desc
                limit 10
                offset %s               
        '''

        self.cursor.execute(sql, (user_id, page * 10, ))
        responses = self.cursor.fetchall()

        sql = '''
                select count(*)
                from bookmark_tb
                where user_id = %s        
        '''

        self.cursor.execute(sql, (user_id,))
        bookmark_count = self.cursor.fetchone()

        return responses, bookmark_count

    def find_in_title(self, user_id, keyword):
        sql = '''
                select *
                from bookmark_tb b
                left outer join memo_tb m on b.id = m.bookmark_id
                where b.user_id = %s and b.title like %s
                order by b.created_at desc
        '''

        self.cursor.execute(sql, (user_id, f'{"%" + keyword + "%"}', ))
        responses = self.cursor.fetchall()

        sql = '''
                select count(*)
                from bookmark_tb
                where user_id = %s and title like %s
        '''

        self.cursor.execute(sql, (user_id, f'{"%" + keyword + "%"}', ))
        bookmark_count = self.cursor.fetchone()

        return responses, bookmark_count

    def find_in_title_and_memo(self, user_id, keyword):
        sql = '''
                select *
                from bookmark_tb b
                left outer join memo_tb m on b.id = m.bookmark_id
                where b.user_id = %s 
                    and (b.title like %s or m.content like %s)
                order by b.created_at desc
        '''

        self.cursor.execute(sql, (user_id, f'{"%" + keyword + "%"}', f'{"%" + keyword + "%"}', ))
        responses = self.cursor.fetchall()

        sql = '''
                select count(*)
                from bookmark_tb
                where user_id = %s and title like %s
        '''

        self.cursor.execute(sql, (user_id, f'{"%" + keyword + "%"}', ))
        bookmark_count = self.cursor.fetchone()

        return responses, bookmark_count

    def delete(self, user_id, url):
        self.connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)

        try:
            sql = '''
                    begin;
                    
                    delete from memo_tb m
                    where m.bookmark_id in (
                        select b.id
                        from bookmark_tb b
                        where b.user_id = %s and b.url = %s
                    );
                    
                    delete from bookmark_tb
                    where user_id = %s and url = %s;
                    
                    commit;
            '''

            self.cursor.execute(sql, (user_id, url, user_id, url, ))
            self.connection.commit()

        except Exception as e:
            self.connection.rollback()
            raise e
