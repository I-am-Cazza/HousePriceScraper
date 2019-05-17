from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def main():
    print(get_average_price())

def get_average_price():
    prices = list()
    page = get_page("https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E87490&maxBedrooms=4&minBedrooms=1&sortType=6&includeSSTC=false")
    prices = get_rightmove_prices(page)
    average = sum(prices)/len(prices)
    return "£" + "{:,.2f}".format(average)


def get_rightmove_prices(html):
    prices = list()
    for div in html.find_all("div"):
        if "class" in div.attrs and "propertyCard-priceValue" in div["class"]:
            price = convert_price(str(div.string))
            if price is not None:
                prices.append(price)
    return prices


def convert_price(str_price: str):
    float_price = ""
    for c in str_price:
        if c in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]:
            float_price = float_price + str(c)
    try:
        return float(float_price)
    except ValueError:
        return None


#  Returns the HTML of the page at <url>
def get_page(url: str):
    try:
        with closing(get(url)) as response:
            if is_valid_response(response):
                return BeautifulSoup(response.content, "html.parser")
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
