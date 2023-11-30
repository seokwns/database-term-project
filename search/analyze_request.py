import re


class AnalyzeRequest:
    def __init__(self, link, title, description, postdate, bloggerId, bloggername):
        self.link = link
        self.title = title
        self.description = description
        self.postdate = postdate
        self.bloggerId = bloggerId
        self.bloggername = bloggername


def convert(response):
    return [
        AnalyzeRequest(
            item['link'].replace("\\", ""),
            item['title'],
            item['description'],
            item['postdate'],
            extract_blogger_id(item['bloggerlink']),
            item['bloggername']
        )
        for item in response['items']
        if 'blog.naver.com' in item['link']
    ]


def extract_blogger_id(bloggerlink):
    match = re.search(r"/([^/]+)$", bloggerlink)
    return match.group(1) if match else ""
