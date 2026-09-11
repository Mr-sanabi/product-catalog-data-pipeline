# Product Catalog Data Pipeline

A Python 3.11+ learning project that combines Books to Scrape data and a local Amazon CSV, normalizes records, and exports validation results and summaries.

## Run

```bash
python -m pip install -r requirements.txt
python -m src.main --book-pages 2
```

For local data, use `--amazon-csv data/raw/amazon-products.csv` and optional `--amazon-limit 100`, alone or with `--book-pages`. The dataset is not included.
Expected CSV columns: `asin`, `title`, `brand`, `categories`, `final_price`, `currency`, `availability`, `rating`, `url`.

## Output

CSV: `data/processed/products.csv`; JSON: `data/processed/pipeline_result.json`; report: `reports/pipeline_report.md`.
JSON contains accepted records, rejected records, analysis, and run statistics. Use `python -m src.main --help` for custom paths.
[Record schema](docs/product_schema.md) · [Example report](docs/example_report.md)

## Limits

Amazon input is a file, not live scraping. Price parsing targets English-style numbers; currencies are not converted or averaged together. Records without a stable ID or URL are kept rather than deduplicated. No database, API, or scheduler.

## Tests

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```
