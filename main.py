from requests import get
from requests.exceptions import RequestException
from contextlib import closing


#  Returns the HTML of the page at <url>
def get_page(url: str):
    try:
        with closing(get(url)) as response:
            if is_valid_response(response):
                return response.content
            else:
                return None
    except RequestException:
        print("Error: Could not connect to " + url)


#  Returns True if <response> contains HTML
def is_valid_response(response) -> bool:
    content_type = response.headers["Content-Type"]
    return (response.status_code == 200 and
            content_type is not None and
            content_type.find("html") != -1)
