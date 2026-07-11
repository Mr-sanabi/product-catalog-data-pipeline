def generate_markdown_report(result):
    lines = []
    stats = result["pipeline_stats"]
    analysis = result["analysis"]
    source_counts = analysis["source_counts"]
    availability_counts = analysis["availability_counts"]
    currency_counts = analysis["currency_counts"]
    price_statistics = analysis["price_stats_by_currency"]
    average_rating = analysis["average_rating"]
    missing_values = analysis["missing_values"]
    lines.append("# Product Catalog Data Pipeline Report")
    lines.append("")
    lines.append("## Run Summary")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|---|---:|")
    lines.append(f"| Raw records | {stats['total_raw_records']} |")
    lines.append(f"| Valid before deduplication | {stats['valid_before_dedup']} |")
    lines.append(f"| Rejected records | {stats['rejected_records']} |")
    lines.append(f"| Duplicates removed | {stats['duplicates_removed']} |")
    lines.append(f"| Final records | {stats['final_records']} |")
    lines.append("")
    lines.append("## Source Breakdown")
    lines.append("")
    lines.append("| Source | Records |")
    lines.append("|---|---:|")

    for source, count in sorted(source_counts.items()):
        lines.append(f"| {source} | {count} |")

    lines.append("")
    lines.append("## Availability")
    lines.append("")
    lines.append("| Status | Records |")
    lines.append("|---|---:|")

    for status, count in sorted(availability_counts.items()):
        lines.append(f"| {status} | {count} |")
    
    lines.append("")

    lines.append("## Currency Breakdown")
    lines.append("")

    lines.append("| Currency | Records |")
    lines.append("|---|---:|")

    for currency, count in sorted(currency_counts.items()):
        lines.append(f"| {currency} | {count} |")
    
    lines.append("")
    lines.append("## Price Statistics")
    lines.append("")
    lines.append("| Currency | Count | Minimum | Maximum | Average |")
    lines.append("|---|---:|---:|---:|---:|")

    for currency, price_stats in sorted(price_statistics.items()):
        lines.append(f"| {currency} | {price_stats['count']} | {price_stats['min']:.2f} | {price_stats['max']:.2f} | {price_stats['average']:.2f} |")
    
    lines.append("")
    lines.append("## Data Quality")
    lines.append("")
    if average_rating is not None:
        lines.append(f"Average rating: **{average_rating:.2f}**")
    else:
        lines.append(f"Average rating: **N/A**")

    lines.append("")


    if missing_values:
        lines.append("| Missing field | Records |")
        lines.append("|---|---:|")
        for field, count in sorted(missing_values.items()):
            lines.append(f"| {field} | {count} |")
    else:
        lines.append("No missing values detected.")

    return "\n".join(lines)