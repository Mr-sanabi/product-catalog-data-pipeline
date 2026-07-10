import requests
import logging
from bs4 import BeautifulSoup


def fetch_html(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        response.encoding = "utf-8"
        return response.text
    
    except requests.exceptions.RequestException as error:
        logging.error(f"Request error on {url}: {error}")
        return None


def get_text_or_none(parent, selector):
    tag = parent.select_one(selector)
    if tag:
        return tag.get_text(strip=True)
    else:
        return None
    
def get_attr_or_none(parent, selector, attr):
    tag = parent.select_one(selector)
    if tag and tag.has_attr(attr):
        return tag[attr]
    else:
        return None

def extract_book(card):
    title = get_attr_or_none(card, "h3 a", "title")
    price = get_text_or_none(card, ".price_color")
    availability = get_text_or_none(card, ".availability")
    rating_tag = card.select_one("p.star-rating")
    product_url = get_attr_or_none(card, "h3 a", "href")

    if rating_tag and rating_tag.has_attr("class"):
        rating = rating_tag["class"][1]
    else:
        rating = None
    
    return {
        "title_raw": title,
        "price_raw": price,
        "availability_raw": availability,
        "rating_raw": rating,
        "product_url_raw": product_url
    }

def parse_page(html):
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select(".product_pod")
    books = []
    for card in cards:
        books_list = extract_book(card)
        books.append(books_list)

    return books

def load_books(max_pages):
    all_books = []
    for page_number in range(1, max_pages + 1):
        logging.info(f"Scraping page: {page_number}...")
        page_url = f"https://books.toscrape.com/catalogue/page-{page_number}.html"
        html = fetch_html(page_url)
        if not html:
            logging.warning(f"Warning this page is empty: {page_number}")
            continue
        
        books = parse_page(html)
        if not books:
            logging.warning(f"No books found on page: {page_number}")
            continue

        all_books.extend(books)
    
    return all_books