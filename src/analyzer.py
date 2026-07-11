from collections import Counter, defaultdict

def analyze_records(records):
    total_records = len(records)
    
    source_counts = Counter()
    availability_counts = Counter()
    currency_counts = Counter()
    missing_values = Counter()

    prices_by_currency = defaultdict(list)
    price_stats_by_currency = {}
    ratings = []

    fields_to_check = [
        "source_id",
        "title",
        "brand",
        "category",
        "price",
        "currency",
        "rating",
        "product_url",
    ]

    for record in records:
        source = record.get("source")
        source_counts[source] +=1
        availability = record.get("availability")
        availability_counts[availability] +=1
        currency = record.get("currency")
        currency_counts[currency] +=1

        price = record.get("price")
        if price is not None and currency is not None:
            prices_by_currency[currency].append(price)
        
        rating = record.get("rating")
        if rating is not None:
            ratings.append(rating)

        for field in fields_to_check:
            value = record.get(field)
            if value is None:
                missing_values[field] +=1
    if ratings:
        average_rating = sum(ratings) / len(ratings)
    else:
        average_rating = None
    for currency, prices in prices_by_currency.items():
        price_stats_by_currency[currency] = {
            "count": len(prices), 
            "min": min(prices),
            "max": max(prices), 
            "average": sum(prices) / len(prices)
        }
    return {
        "total_records": total_records,
        "source_counts": dict(source_counts),
        "availability_counts": dict(availability_counts),
        "currency_counts": dict(currency_counts),
        "price_stats_by_currency": dict(price_stats_by_currency),
        "average_rating": average_rating,
        "missing_values": dict(missing_values)
        }