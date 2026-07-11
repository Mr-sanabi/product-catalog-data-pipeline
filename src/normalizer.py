from urllib.parse import urljoin
import json
from datetime import datetime, timezone

def normalize_text(value):
    if value is None:
        return None
    
    cleaned_value = value.strip()

    if cleaned_value:
        return " ".join(cleaned_value.split())

    return None

def normalize_price(value):
    if value is None:
        return None
    
    cleaned_value = value.strip()
    cleaned_value = cleaned_value.replace("$", "")
    cleaned_value = cleaned_value.replace(",", "")
    cleaned_value = cleaned_value.replace('"', "")
    cleaned_value = cleaned_value.replace("£", "")
    cleaned_value = cleaned_value.replace("€", "")

    try:
        number = float(cleaned_value)
        return number
    except ValueError:
        return None
    
def normalize_currency(value, price_raw=None):
    if value:
        cleaned_value = value.strip()
        cleaned_value = cleaned_value.upper()
        if len(cleaned_value) == 3:
            return cleaned_value
        
    if price_raw is not None:
        if "£" in price_raw:
            return "GBP"
              
        elif "$" in price_raw:
            return "USD"

        elif "€" in price_raw:
            return "EUR"
            
    return None
        

def normalize_availability(value):
    out_of_stock_phrases = [
    "out of stock",
    "currently unavailable",
    "not in stock",
    ]

    in_stock_phrases = [
        "in stock",
    ]


    cleaned_value = normalize_text(value)

    if cleaned_value is None:
        return "unknown"

    cleaned_value = cleaned_value.lower()

    is_out = any(phrase in cleaned_value for phrase in out_of_stock_phrases)
    if is_out:
        return "out_of_stock"

    is_in = any(phrase in cleaned_value for phrase in in_stock_phrases)
    if is_in:
        return "in_stock"
    
    return "unknown"

def normalize_rating(value):
    rating_words = {
        "one": 1.0,
        "two": 2.0,
        "three": 3.0,
        "four": 4.0,
        "five": 5.0,
    }

    cleaned_value = normalize_text(value)

    if cleaned_value is None:
        return None
    
    cleaned_value = cleaned_value.lower()

    if cleaned_value in rating_words:
        return rating_words[cleaned_value]
    else:
        try:
            number = float(cleaned_value)
            return number    
        except ValueError:
            return None
        
def normalize_url(value, base_url=None):
    cleaned_value = normalize_text(value)
    
    if cleaned_value is None:
        return None
    
    if base_url:
        new_url = urljoin(base_url, cleaned_value)
        return new_url
    else:
        return cleaned_value
    
def normalize_category(value):
    cleaned_value = normalize_text(value)

    if cleaned_value is None:
        return None
    try:
        parsed = json.loads(cleaned_value)

        if isinstance(parsed, list):
            if not parsed:
                return None

            last_element = parsed[-1]
            return normalize_text(str(last_element))

        return cleaned_value
    
    except json.JSONDecodeError:
        return cleaned_value
    
def normalize_record(raw_record, source, base_url=None, collected_at=None):
    if collected_at is None:
        final_collected_at = datetime.now(timezone.utc).isoformat()
    else:
        final_collected_at = collected_at
    return {
        "source": source,
        "source_id": normalize_text(raw_record.get("source_id_raw")),
        "title": normalize_text(raw_record.get("title_raw")),
        "brand": normalize_text(raw_record.get("brand_raw")),
        "category": normalize_category(raw_record.get("category_raw")),
        "price_raw": raw_record.get("price_raw"),
        "price": normalize_price(raw_record.get("price_raw")),
        "currency": normalize_currency(raw_record.get("currency_raw"), raw_record.get("price_raw")),
        "availability_raw": raw_record.get("availability_raw"),
        "availability": normalize_availability(raw_record.get("availability_raw")),
        "rating": normalize_rating(raw_record.get("rating_raw")),
        "product_url": normalize_url(raw_record.get("product_url_raw"), base_url),
        "collected_at": final_collected_at
        }
