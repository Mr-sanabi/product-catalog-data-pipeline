from pathlib import Path
import csv
import json
CSV_FIELDS = [
    "source",
    "source_id",
    "title",
    "brand",
    "category",
    "price_raw",
    "price",
    "currency",
    "availability_raw",
    "availability",
    "rating",
    "product_url",
    "collected_at",
]


def ensure_parent_directory(file_path):

    path = Path(file_path)

    parent_dir = path.parent

    parent_dir.mkdir(parents=True, exist_ok=True)

def save_csv(file_path, records):

    ensure_parent_directory(file_path)    
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(records)

def save_json(file_path, data):
    ensure_parent_directory(file_path)    
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)