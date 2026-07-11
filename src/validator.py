from urllib.parse import urlparse
from datetime import datetime, timedelta

def validate_record(record):
    errors = []
    
    if not record.get("source"):
        errors.append("missing_source")
    if not record.get("title"):
        errors.append("missing_title")
    
    price = record.get("price")
    if price is not None:
        if not isinstance(price, (int, float)):
            errors.append("invalid_price")
        elif price < 0:
            errors.append("invalid_price")

    currency = record.get("currency")
    if currency is not None:
        if not isinstance(currency, str):
            errors.append("invalid_currency")
        elif len(currency) != 3:
            errors.append("invalid_currency")
        elif not currency.isalpha():
            errors.append("invalid_currency")
        elif not currency.isupper():
            errors.append("invalid_currency")

    allowed_availability = {
        "in_stock",
        "out_of_stock",
        "unknown",
    }
    
    availability = record.get("availability")
    if availability not in allowed_availability:
        errors.append("invalid_availability")

    rating = record.get("rating")
    if rating is not None:
        if not isinstance(rating, (int, float)):
            errors.append("invalid_rating")
        elif not 0 <= rating <= 5:
            errors.append("invalid_rating")

    product_url = record.get("product_url")
    if product_url is not None:
        if not isinstance(product_url, str):
            errors.append("invalid_product_url")
        else:
            parsed = urlparse(product_url)
            if parsed.scheme not in {"https", "http"}:
                errors.append("invalid_product_url")
            elif not parsed.netloc:
                errors.append("invalid_product_url")

    collected_at = record.get("collected_at")
    if not isinstance(collected_at, str) or not collected_at:
            errors.append("invalid_collected_at")
    else:
        try:
            parsed_time = datetime.fromisoformat(collected_at)
        except ValueError:
            errors.append("invalid_collected_at")

        else:
            if parsed_time.utcoffset() != timedelta(0):
                errors.append("invalid_collected_at")

    return errors

