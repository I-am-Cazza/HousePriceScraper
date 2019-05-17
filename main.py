from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup


# Returns the average house price in London, formatted as "£00,000.00"
def main():
    print("£" + "{:,.2f}".format(get_average_price()))


# Finds the average price of houses in London according to the supported websites
def get_average_price() -> float:
    page = get_page("https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E87490&sortType=6&propertyTypes=detached%2Csemi-detached%2Cterraced&primaryDisplayPropertyType=houses&includeSSTC=false")
    prices = get_prices(page, "rightmove")
    page = get_page("https://www.zoopla.co.uk/for-sale/houses/london/?page_size=100&q=London&radius=0&results_sort=newest_listings&search_source=refine")
    prices.extend(get_prices(page, "zoopla"))
    average = sum(prices)/len(prices)
    return average


# Returns a list of all the prices found at the given site
def get_prices(html, site_name) -> list:
    prices = list()

    # Select the correct tags and attributes to find the prices for a given site
    if site_name == "rightmove":
        tag_type = "div"
        class_name = "propertyCard-priceValue"
    else:
        tag_type = "a"
        class_name = "listing-results-price"

    # Find every price on the page and add them all to a list as floats
    for tag in html.find_all(tag_type):
        if "class" in tag.attrs and class_name in tag["class"]:
            price = convert_price(str(tag.string))
            if price is not None:
                prices.append(price)
    return prices


# Converts the string price in the format "£00,000,000.00" to a float
def convert_price(str_price: str):
    float_price = ""
    for c in str_price:
        if c in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]:
            float_price = float_price + str(c)
    try:
        return float(float_price)
    except ValueError:
        return None


# Returns the HTML of the page at <url>
def get_page(url: str):
    try:
        with closing(get(url)) as response:
            if is_valid_response(response):
                return BeautifulSoup(response.content, "html.parser")
            else:
                return None
    except RequestException:
        print("Error: Could not connect to " + url)


# Returns True if <response> contains HTML
def is_valid_response(response) -> bool:
    content_type = response.headers["Content-Type"]
    return (response.status_code == 200 and
            content_type is not None and
            content_type.find("html") != -1)
