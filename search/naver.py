import requests
from .blog_post_dto import BlogPostDTO
from .html_parser import parse_html
from .html_parser import extract_text_from_items


def search_keyword(connection, cursor, keyword, number):
    client_id = '_________________'
    client_secret = '__________________'
    headers = {'X-Naver-Client-Id': 'YoL5w1HC7dqiP6qgYOqn', 'X-Naver-Client-Secret': 'ybbtS8rMQN'}

    base_url = "https://openapi.naver.com/v1/search/blog.json?query="
    cursor = "$&start="

    url = base_url + keyword + cursor + str(number*10 - 9)

    response = requests.get(url, headers=headers).json()
    posts = parse_json(response)

    for post in posts:
        items = parse_html(post)
        text = extract_text_from_items(items)

    return posts


def parse_json(response):
    blog_posts = []

    for item in response['items']:
        title = item['title']
        link = item['link']
        description = item['description']
        bloggername = item['bloggername']
        bloggerlink = item['bloggerlink']
        postdate = item['postdate']

        blog_post = BlogPostDTO(title, link, description, bloggername, bloggerlink, postdate)
        blog_posts.append(blog_post)

    return blog_posts
