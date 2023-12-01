import re


class BlogPostDTO:
    def __init__(self, title, link, description, bloggername, bloggerlink, postdate, advertisement, confidence):
        self.title = self.remove_html_tags(title)
        self.link = link
        self.description = self.remove_html_tags(description)
        self.bloggername = bloggername
        self.bloggerlink = bloggerlink
        self.postdate = postdate
        self.advertisement = advertisement
        self.confidence = confidence

    def remove_html_tags(self, input_string):
        clean_text = re.sub('<.*?>', '', input_string)
        return clean_text
