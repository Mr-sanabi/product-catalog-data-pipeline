def build_dedup_key(record):
    source_id = record.get("source_id")

    if source_id:
        return (
            "source_id",
            record.get("source"),
            source_id
        )
    
    product_url = record.get("product_url")
    
    if product_url:
        return ("product_url", product_url)
    
    return None

def deduplicate_records(records):
    result = []
    seen = set()
    dubls = 0 
    for record in records:
        key = build_dedup_key(record)
        if key is None:
            result.append(record)
        elif key in seen:
            dubls+=1
        else:
            seen.add(key)
            result.append(record)
    
    return result, dubls