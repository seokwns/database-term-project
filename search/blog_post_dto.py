import re


class BlogPostDTO:
    def __init__(self, title, link, description, bloggername, bloggerlink, postdate, advertisement, confidence):
        self.title = self.remove_html_tags(title)
        self.link = link
        self.description = self.remove_html_tags(description)
        self.bloggername = bloggername
        self.bloggerlink = bloggerlink
        self.bloggerid = self.get_blogger_id(bloggerlink)
        self.postdate = postdate
        self.advertisement = advertisement
        self.confidence = confidence

    @staticmethod
    def remove_html_tags(input_string):
        clean_text = re.sub('<.*?>', '', input_string)
        return clean_text

    @staticmethod
    def get_blogger_id(link):
        blogger_id = ""

        matcher = re.search(r'/([^/]+)$', link)
        if matcher:
            blogger_id = matcher.group(1)

        return blogger_id
