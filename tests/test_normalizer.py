from src.normalizer import normalize_text, normalize_price, normalize_availability, normalize_currency, normalize_rating, normalize_url
import pytest


text = "  Running    shoes\nfor men  "

def test_normalize_text_collapses_whitespace():
    result = normalize_text(text)
    assert result == "Running shoes for men"

price = "£51.77"

def test_normalize_price():
    result = normalize_price(price)
    assert result == 51.77

avilability = "Out of stock"

def test_normalize_availability():
    result = normalize_availability(avilability)
    assert result == "out_of_stock"

@pytest.mark.parametrize(
    "value, expected",
    [
        (None, None),
        ("", None),
        ("£51.77", 51.77),
        ("$1,299.50", 1299.5),
        ('\"57.79\"', 57.79),
        ("not available", None)
    ],
)
def test_normalize_price(value, expected):
    result = normalize_price(value)
    assert result == expected

@pytest.mark.parametrize(
    "value, price_raw, expected",
    [
        ("usd", None, "USD"),
        (" EUR ", None, "EUR"),
        (None, "£51.77", "GBP"),
        (None, "$25.00", "USD"),
        (None, "100.00", None),
        ("dollars", None, None)
    ],
)
def test_normalize_price(value, price_raw, expected):
    result = normalize_currency(value, price_raw)
    assert result == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (None, None),
        ("Three", 3.0),
        (" five ", 5.0),
        ("4.6", 4.6),
        ("not rated", None),
    ],
)
def test_normalize_price(value, expected):
    result = normalize_rating(value)
    assert result == expected


@pytest.mark.parametrize(
    "value, base_url, expected",
    [
        (None, None, None),
        ("book/index.html" , "https://site.com/catalogue/", "https://site.com/catalogue/book/index.html"),
        ("https://amazon.com/item", None, "https://amazon.com/item"),
    ],
)
def test_normalize_price(value, base_url, expected):
    result = normalize_url(value, base_url)
    assert result == expected