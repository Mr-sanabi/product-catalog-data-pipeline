import pytest
from src.deduplicator import build_dedup_key, deduplicate_records

test_id = {
    "source": "test_store",
    "source_id": "X123",
    "product_url": "https://example.com/products/x123",
}


def test_build_key_prefers_source_id():
    key = build_dedup_key(test_id)
    assert key == ("source_id", "test_store", "X123")

test_url = {
    "source": "test_store",
    "source_id": None,
    "product_url": "https://example.com/products/x123",
}

def test_build_key_uses_url_as_fallback():
    key = build_dedup_key(test_url)
    assert key == ("product_url", "https://example.com/products/x123")


test_none = {
    "source": "test_store",
    "source_id": None,
    "product_url": None,
}

def test_build_key_returns_none_without_identity():
    key = build_dedup_key(test_none)
    assert key is None

records = [
    {
        "source": "amazon_csv",
        "source_id": "A1",
        "product_url": "https://example.com/amazon/first",
        "title": "Amazon first",
    },
    {
        "source": "amazon_csv",
        "source_id": "A1",
        "product_url": "https://example.com/amazon/duplicate",
        "title": "Amazon duplicate",
    },
    {
        "source": "books_to_scrape",
        "source_id": None,
        "product_url": "https://example.com/book",
        "title": "Book first",
    },
    {
        "source": "books_to_scrape",
        "source_id": None,
        "product_url": "https://example.com/book",
        "title": "Book duplicate",
    },
    {
        "source": "unknown",
        "source_id": None,
        "product_url": None,
        "title": "Unknown A",
    },
    {
        "source": "unknown",
        "source_id": None,
        "product_url": None,
        "title": "Unknown B",
    },
]

def test_deduplicate_records_removes_only_stable_duplicates():

    unique_records, duplicates_removed = deduplicate_records(records)
    titles = []
    for record in unique_records:
        titles.append(record["title"])
    assert "Unknown A" in titles
    assert "Unknown B" in titles