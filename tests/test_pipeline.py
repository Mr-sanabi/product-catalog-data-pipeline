import pytest
from src.pipeline import process_records

valid_raw_record = {
    "source_id_raw": "A1",
    "title_raw": "  Example    Product  ",
    "brand_raw": "Example Brand",
    "category_raw": '["Products", "Test Category"]',
    "price_raw": "$20.00",
    "currency_raw": "usd",
    "availability_raw": "In stock",
    "rating_raw": "4.5",
    "product_url_raw": "item.html",
}

def test_process_records_normalizes_and_accepts_valid_record():
    valid_records, rejected_records = process_records(
        [valid_raw_record],
        source="test_source",
        base_url="https://example.com/catalogue/",
        collected_at="2026-07-12T10:00:00+00:00",
    )
    assert len(valid_records) == 1
    assert rejected_records == []


def test_process_records_rejects_invalid_raw_contract():
    invalid_raw_record = {
        "title_raw": "Broken Product",
    }
    valid_records, rejected_records = process_records(
        [invalid_raw_record],
        source="test_source",
        collected_at="2026-07-12T10:00:00+00:00",
    )
    assert valid_records == []
    assert len(rejected_records) == 1
    assert rejected_records[0]["normalized_record"] is None
    assert rejected_records[0]["errors"] == ["invalid_raw_contract"]