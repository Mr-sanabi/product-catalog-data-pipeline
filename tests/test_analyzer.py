import pytest
from src.analyzer import analyze_records

records = [
    {
        "source": "amazon",
        "source_id": "A1",
        "title": "Running Shoes",
        "brand": None,
        "category": "Running",
        "price": 10.0,
        "currency": "USD",
        "availability": "in_stock",
        "rating": 4.0,
        "product_url": "https://example.com/amazon/a1",
    },
    {
        "source": "amazon",
        "source_id": "A2",
        "title": "Winter Jacket",
        "brand": "Example Brand",
        "category": None,
        "price": 20.0,
        "currency": "USD",
        "availability": "out_of_stock",
        "rating": None,
        "product_url": None,
    },
    {
        "source": "books",
        "source_id": None,
        "title": "Example Book",
        "brand": None,
        "category": None,
        "price": 30.0,
        "currency": "GBP",
        "availability": "in_stock",
        "rating": 2.0,
        "product_url": "https://example.com/books/example-book",
    },
]

def test_analyze_records_returns_expected_statistics():
    result = analyze_records(records)
    assert result["total_records"] == 3 
    assert result["source_counts"]["amazon"] == 2
    assert result["source_counts"]["books"] == 1
    assert result["availability_counts"]["in_stock"] == 2
    assert result["currency_counts"]["USD"] == 2
    assert result["price_stats_by_currency"]["USD"]["average"] == 15.0
    assert result["price_stats_by_currency"]["GBP"]["average"] == 30.0
    assert result["average_rating"] == 3.0
    assert result["missing_values"]["brand"] == 2
    assert result["missing_values"]["category"] == 2