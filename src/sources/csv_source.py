import csv
import logging

def load_amazon_csv(file_path, limit=None):
    raw_records = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            csv.field_size_limit(10_000_000)
            rows = csv.DictReader(file)
            for row in rows:
                if limit is not None and len(raw_records) >= limit:
                    break
                raw_record = {
                "source_id_raw": clean_raw_value(row.get("asin")),
                "title_raw": clean_raw_value(row.get("title")),
                "brand_raw": clean_raw_value(row.get("brand")),
                "category_raw": clean_raw_value(row.get("categories")),
                "price_raw": clean_raw_value(row.get("final_price")), 
                "currency_raw": clean_raw_value(row.get("currency")),
                "availability_raw": clean_raw_value(row.get("availability")),
                "rating_raw": clean_raw_value(row.get("rating")),
                "product_url_raw": clean_raw_value(row.get("url"))
                }
                raw_records.append(raw_record)
            
            return raw_records
        
    except (FileNotFoundError, OSError, csv.Error) as e:
        logging.error(f"Failed to load CSV file '%s': %s", file_path, str(e))
        return []


def clean_raw_value(value):
    if value == None:
        return None
    cleaned_value = value.strip()
    if not cleaned_value:
        return None
    else:
        return cleaned_value