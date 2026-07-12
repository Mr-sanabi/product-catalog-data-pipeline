import pytest
from src.validator import validate_record


def make_valid_record():
    valid_record   =   {
      "source": "amazon_csv",
      "source_id": "B00080QHMM",
      "title": "Accutire MS-4021B Digital Tire Pressure Gauge with 4 Valve Caps, 5-150psi (psi, bar, kPa, kg/cm2)",
      "brand": "Accutire",
      "category": "Tire Repair Tools",
      "price_raw": "1.795000000000000e+01",
      "price": 17.95,
      "currency": "USD",
      "availability_raw": "In Stock",
      "availability": "in_stock",
      "rating": 4.4,
      "product_url": "https://www.amazon.com/dp/B00080QHMM?th=1&psc=1&currency=USD&language=en_GB",
      "collected_at": "2026-07-11T20:40:56.918247+00:00"
    }
    return valid_record

# def test_valid_record_has_no_errors():
#     result = validate_record(make_valid_record())
#     assert result == []

@pytest.mark.parametrize(
    "field, invalid_value, expected_error",
    [
        ("source", None, "missing_source"),
        ("title", None, "missing_title"),
        ("price", "-1", "invalid_price"),
        ("price", "20.00", "invalid_price"),
        ("currency", "usd", "invalid_currency"),
        ("availability", "preorder", "invalid_availability"),
        ("rating", 6, "invalid_rating"),
        ("product_url", "item.html", "invalid_product_url"),
        ("collected_at", "2026-07-12T10:00:00", "invalid_collected_at")
    ],
)
def test_invalid_field_returns_expected_error(field, invalid_value, expected_error):
    record = make_valid_record()
    record[field] = invalid_value
    result = validate_record(record)
    assert expected_error in result