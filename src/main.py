import argparse
from src.pipeline import run_pipeline
from pprint import pprint
from src.writer import save_csv, save_json, save_text
from src.report import generate_markdown_report
from src.logging_config import setup_logging
import logging

def non_negative_int(value):
    try:
        page_value = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("Number of pages must be an integer")
    if page_value >= 0:
        return page_value
    else:
        raise argparse.ArgumentTypeError("Number of pages must be greater than or equal to 0")
    
def positive_int(value):
        try:
            page_value = int(value)
        except ValueError:
            raise argparse.ArgumentTypeError("Number of pages must be an integer")
        if page_value > 0:
            return page_value
        else:
            raise argparse.ArgumentTypeError("Number of pages must be greater than 0")

def parse_args():

    parser = argparse.ArgumentParser(
        description=
            "Load product data from web and CSV sources, normalize and validate "
            "records, remove duplicates, and generate dataset analytics."
        )
    parser.add_argument("--book-pages", default=0, type=non_negative_int, help="number of Books pages; 0 disables the source")
    parser.add_argument("--amazon-csv", default=None, type=str, help="Path to Amazon CSV")
    parser.add_argument("--amazon-limit", default=None, type=positive_int, help="Rows limit for Amazon")
    parser.add_argument("--csv-output", default="data/processed/products.csv", help="CSV output path")
    parser.add_argument("--json-output", default="data/processed/pipeline_result.json", help="JSON output path")
    parser.add_argument("--report-output", default="reports/pipeline_report.md", help="Report output path")


    parser_result = parser.parse_args()
    if parser_result.book_pages == 0 and not parser_result.amazon_csv:
        parser.error("At least one source must be selected: use --book-pages or --amazon-csv.")
    return parser_result

def main():
    args = parse_args()
    setup_logging()
    
    result = run_pipeline(args.book_pages, args.amazon_csv, args.amazon_limit)
    final_records = result["pipeline_stats"]["final_records"]
    if final_records == 0:
        logging.warning("Pipeline produced no final records.")
    report = generate_markdown_report(result)
    try:
        save_csv(args.csv_output, result["records"])
        save_json(args.json_output, result)
        save_text(args.report_output, report)
    except OSError as e:
        logging.error(f"Failed to save output files: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()