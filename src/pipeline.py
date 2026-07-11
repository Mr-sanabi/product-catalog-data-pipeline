from src.validator import validate_record
from src.normalizer import normalize_record
from src.sources.contracts import validate_raw_record
from src.sources.books_source import load_books
from src.sources.csv_source import load_amazon_csv
from src.deduplicator import deduplicate_records
from src.analyzer import analyze_records
from datetime import datetime, timezone

def process_records(raw_records, source, base_url=None, collected_at=None):
    valid_records = []
    rejected_records = []
    for raw_record in raw_records:
        result = validate_raw_record(raw_record)
        if result is False:
            rejected_records.append({
                "raw_record": raw_record,
                "normalized_record": None,
                "errors": ["invalid_raw_contract"] 
            })
            continue
        
        normalized_record = normalize_record(raw_record, source, base_url=base_url, collected_at=collected_at)
        errors = validate_record(normalized_record)
        if errors:
            rejected_records.append({
                "raw_record": raw_record,
                "normalized_record": normalize_record,
                "errors": errors})
        else:
            valid_records.append(normalized_record)
        
    return valid_records, rejected_records

def run_pipeline(book_pages=0, amazon_csv_path=None, amazon_limit=None):
    batch_collected_at = datetime.now(timezone.utc).isoformat()
    all_valid_records = []
    all_rejected_records = []
    total_raw_records = 0

    if book_pages > 0:
        books = load_books(book_pages)
        total_raw_records += len(books)
        books_valid, books_rejected = process_records(books, source="books_to_scrape", base_url="https://books.toscrape.com/catalogue/", collected_at=batch_collected_at)
        all_valid_records.extend(books_valid)
        all_rejected_records.extend(books_rejected)
    
    if amazon_csv_path:
        amazon_data = load_amazon_csv(amazon_csv_path, amazon_limit)
        total_raw_records += len(amazon_data)
        data_valid, data_rejected = process_records(amazon_data, source="amazon_csv", base_url=None, collected_at=batch_collected_at)
        all_valid_records.extend(data_valid)
        all_rejected_records.extend(data_rejected)

    unique_records, duplicates_removed = deduplicate_records(all_valid_records)
    analysis = analyze_records(unique_records)
    pipeline_stats = {
        "total_raw_records": total_raw_records,
        "valid_before_dedup": len(all_valid_records),
        "rejected_records": len(all_rejected_records),
        "duplicates_removed": duplicates_removed, 
        "final_records": len(unique_records)
        }
    
    return {
        "records": unique_records,
        "rejected_records": all_rejected_records,
        "analysis": analysis,
        "pipeline_stats": pipeline_stats
    }
    

        