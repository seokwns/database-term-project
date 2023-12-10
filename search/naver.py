import requests
import re
from .blog_post_dto import BlogPostDTO
from .html_parser import parse_html
from .html_parser import extract_text_from_items


def search_keyword(keyword, number, vectorizer, model):
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

        text = preprocessing(text)
        tokenized = tokenizing(vectorizer, text)
        prediction = model.predict(tokenized)[0]
        prediction_probabilities = model.predict_proba(tokenized)[0]

        post.advertisement = prediction
        post.confidence = prediction_probabilities

    return posts


def preprocessing(text):
    # 영어 대소문자, 숫자, 한글을 제외한 모든 문자 제거
    text = re.sub('[^A-Za-z0-9가-힣]', '', text)
    # 특정 기호들 제거
    text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', text)
    # 개행 문자 제거
    text = re.sub('\n', '', text)

    return text[-200:]


def tokenizing(vectorizer, text):
    return vectorizer.transform([text])


def parse_json(response):
    blog_posts = []

    for item in response['items']:
        title = item['title']
        link = item['link']
        description = item['description']
        bloggername = item['bloggername']
        bloggerlink = item['bloggerlink']
        postdate = item['postdate']
        advertisement = False
        confidence = 0

        blog_post = BlogPostDTO(
            title,
            link,
            description,
            bloggername,
            bloggerlink,
            postdate,
            advertisement,
            confidence
        )
        blog_posts.append(blog_post)

    return blog_posts
