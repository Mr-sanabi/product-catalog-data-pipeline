RAW_RECORD_FIELDS = set(["source_id_raw", "title_raw", "brand_raw", "category_raw", "price_raw", "currency_raw", "availability_raw", "rating_raw", "product_url_raw"])

def validate_raw_record(record):
    if set(record.keys()) == RAW_RECORD_FIELDS:
        return True
    else:
        return False