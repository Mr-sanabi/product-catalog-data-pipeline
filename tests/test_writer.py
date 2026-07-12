import pytest
import csv, json
from src.writer import save_csv, save_json, CSV_FIELDS

data = {
    "records": [{"source": "test", "title": "Product"}],
    "analysis": {"total_records": 1},
}

def test_save_json_round_trip(tmp_path):
    file_path = tmp_path / "output" / "data.json"
    save_json(file_path, data)
    assert file_path.exists()
    rows = file_path.read_text(encoding="utf-8")
    loaded = json.loads(rows)
    assert loaded == data

records = [
    {
        "source": "test",
        "title": "Example Product",
    }
]

def test_save_csv_writes_records(tmp_path):
    file_path = tmp_path / "output" / "products.csv"
    save_csv(file_path, records)
    assert file_path.exists()
    with open (file_path, "r",encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    assert len(rows) == 1
    assert rows[0]["source"] == "test"
    assert rows[0]["title"] == "Example Product"


def test_save_csv_writes_header_for_empty_records(tmp_path):
    file_path = tmp_path / "output" / "empty.csv"
    save_csv(file_path, [])
    assert file_path.exists()
    with open (file_path, "r",encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        rows = list(reader)
    assert fieldnames == CSV_FIELDS
    assert rows == []
