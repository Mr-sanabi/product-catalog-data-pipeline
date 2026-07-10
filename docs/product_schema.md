# Normalized Product Schema

## Purpose

This document defines the normalized product record shared by every data source in the pipeline.

Source adapters may return different raw fields and formats. The normalization layer converts every raw record into this common structure before validation, analysis, and export.

## Product Record

| Field | Python Type | Required | Description |
| --- | --- | --- | --- |
| `source` | `str` | Yes | Stable name of the data source. |
| `source_id` | `Optional[str]` | No | Stable product identifier provided by the source. |
| `title` | `str` | Yes | Cleaned product title. |
| `brand` | `Optional[str]` | No | Product brand when available. |
| `category` | `Optional[str]` | No | Product category when available. |
| `price_raw` | `Optional[str]` | No | Original price value received from the source. |
| `price` | `Optional[float]` | No | Parsed numeric price without a currency symbol. |
| `currency` | `Optional[str]` | No | Three-letter currency code such as `GBP`, `USD`, or `PLN`. |
| `availability_raw` | `Optional[str]` | No | Original availability value received from the source. |
| `availability` | `str` | Yes | Normalized availability status. |
| `rating` | `Optional[float]` | No | Normalized numeric rating from `0` to `5`. |
| `product_url` | `Optional[str]` | No | Absolute product URL. |
| `collected_at` | `str` | Yes | Collection timestamp in ISO 8601 UTC format. |

## Missing Values

Missing optional values are represented as `None` inside Python.

Export behavior:

- Python: `None`
- JSON: `null`
- CSV: empty cell

Empty strings must not be used for missing numeric values such as `price` or `rating`.

Required fields must not be `None` or empty after normalization.

## Source Names

The following source names are used in version 1:

- `books_to_scrape`
- `amazon_csv`

Source names must remain consistent across normalized records, reports, logs, and output files.

## Title Normalization

Product titles must:

- have leading and trailing whitespace removed;
- have repeated internal whitespace collapsed into a single space;
- preserve original capitalization;
- preserve punctuation and meaningful symbols.

Example:

```text
Raw:        "  Apple    iPhone 15\nPro  "
Normalized: "Apple iPhone 15 Pro"
```

## Price Normalization

The original price is preserved in `price_raw`.

The normalized price is divided into:

- `price`: numeric value;
- `currency`: three-letter uppercase currency code.

Example:

```text
price_raw: "£51.77"
price: 51.77
currency: "GBP"
```

Currency conversion is outside the scope of version 1.

If a price cannot be parsed safely:

- `price_raw` preserves the original value;
- `price` is set to `None`;
- `currency` is set when it can still be identified reliably.

## Availability Normalization

The source value is preserved in `availability_raw`.

The normalized `availability` field must contain one of:

- `in_stock`
- `out_of_stock`
- `unknown`

Examples:

| Raw Value | Normalized Value |
| --- | --- |
| `In stock` | `in_stock` |
| `Available` | `in_stock` |
| `Na stanie` | `in_stock` |
| `Out of stock` | `out_of_stock` |
| missing or unrecognized value | `unknown` |

Availability mappings are implemented separately for each source adapter.

## Rating Normalization

Ratings are represented as numeric values from `0` to `5`.

Examples:

| Raw Value | Normalized Value |
| --- | --- |
| `One` | `1.0` |
| `Three` | `3.0` |
| `4.5` | `4.5` |
| missing or invalid value | `None` |

Values outside the `0–5` range are invalid.

## Source ID Rules

`source_id` must only contain a stable identifier connected to the original source.

Priority:

1. Use an explicit product ID supplied by the source.
2. Use an ID extracted from a URL only when the URL structure is stable and documented for that source.
3. Otherwise, use `None`.

A source ID must not be generated from the product title because titles can change and multiple products can share the same title.

## Product URL Rules

`product_url` must be:

- an absolute HTTP or HTTPS URL;
- connected to the original product;
- `None` when a reliable URL is unavailable.

Relative URLs must be resolved against the source base URL during normalization.

## Collection Timestamp

`collected_at` uses ISO 8601 UTC:

```text
2026-07-10T19:45:30Z
```

All records collected during one pipeline run may share the same timestamp.

Using UTC prevents ambiguity when the pipeline runs across computers or servers in different time zones.

## Validation Rules

A normalized product is valid when:

- `source` is present;
- `title` is present and not empty;
- `availability` contains an allowed value;
- `price` is `None` or greater than or equal to zero;
- `rating` is `None` or between `0` and `5`;
- `product_url` is `None` or an absolute HTTP/HTTPS URL;
- `collected_at` is present and uses ISO 8601 UTC.

Invalid records are preserved separately with their validation errors. They must not silently disappear from the pipeline.

## Example: Books to Scrape

```json
{
  "source": "books_to_scrape",
  "source_id": "1000",
  "title": "A Light in the Attic",
  "brand": null,
  "category": null,
  "price_raw": "£51.77",
  "price": 51.77,
  "currency": "GBP",
  "availability_raw": "In stock",
  "availability": "in_stock",
  "rating": 3.0,
  "product_url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
  "collected_at": "2026-07-10T19:45:30Z"
}
```

## Example: Amazon CSV

```json
{
  "source": "amazon_csv",
  "source_id": "B0EXAMPLE1",
  "title": "Wireless Computer Mouse",
  "brand": "Example Brand",
  "category": "Computer Accessories",
  "price_raw": "$29.99",
  "price": 29.99,
  "currency": "USD",
  "availability_raw": null,
  "availability": "unknown",
  "rating": 4.5,
  "product_url": "https://www.amazon.com/dp/B0EXAMPLE1",
  "collected_at": "2026-07-10T19:45:30Z"
}
```