from urllib.parse import urljoin

BOOKS_BASE_URL = "https://books.toscrape.com/"
RATING_VALUES = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def clean_books_records(records, base_url=BOOKS_BASE_URL):
    """Normalize Books to Scrape records for output."""
    cleaned_records = []

    for record in records:
        cleaned_records.append(
            {
                "title": _clean_text(record.get("title", "")),
                "price_gbp": _clean_price(record.get("price", "")),
                "availability": _clean_text(record.get("availability", "")),
                "rating": RATING_VALUES.get(_clean_text(record.get("rating", "")), ""),
                "book_url": urljoin(base_url, _clean_text(record.get("book_url", ""))),
                "image_url": urljoin(
                    base_url,
                    _clean_text(record.get("image_url", "")),
                ),
            }
        )

    return cleaned_records


def deduplicate_records(records, key):
    """Return records with duplicate non-empty key values removed."""
    deduplicated_records = []
    seen_values = set()

    for record in records:
        value = record.get(key, "")

        if not value:
            deduplicated_records.append(record)
            continue

        if value in seen_values:
            continue

        seen_values.add(value)
        deduplicated_records.append(record)

    return deduplicated_records


def _clean_text(value):
    """Collapse surrounding whitespace and handle missing values as empty strings."""
    return str(value or "").strip()


def _clean_price(value):
    """Convert a Books to Scrape price string like £51.77 into a float."""
    text = _clean_text(value).replace("£", "")

    if not text:
        return ""

    return float(text)
