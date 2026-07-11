import argparse
from src.pipeline import run_pipeline
from pprint import pprint

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

    parser_result = parser.parse_args()
    if parser_result.book_pages == 0 and not parser_result.amazon_csv:
        parser.error("At least one source must be selected: use --book-pages or --amazon-csv.")
    return parser_result

def main():
    args = parse_args()

    result = run_pipeline(args.book_pages, args.amazon_csv, args.amazon_limit)
    print("Pipeline statistics:")
    pprint(result["pipeline_stats"])
    print("\nDataset analysis:")
    pprint(result["analysis"])


if __name__ == "__main__":
    main()