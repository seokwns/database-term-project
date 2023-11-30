import requests
from bs4 import BeautifulSoup


def parse_html(request):
    splits = request['link'].split("/")
    post_id = splits[-1]
    post_url = f"https://blog.naver.com/PostView.naver?blogId={request['bloggerId']}&logNo={post_id}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.36'
    }

    response = requests.get(post_url, headers=headers)
    if not response.ok:
        return None

    document = BeautifulSoup(response.text, 'html.parser')

    not_sponsored_button = document.select(".not_sponsored_button")
    if not_sponsored_button:
        return None

    items = document.select(f"#post-view{post_id} > div > div > div.se-main-container")

    if not items:
        items = document.select(f"#post-view{post_id} > div > div.se-main-container")

    return items


def extract_text_from_items(items):
    if not items:
        return None

    text_list = [item.get_text() for item in items]

    extracted_text = '\n'.join(text_list)

    return extracted_text
