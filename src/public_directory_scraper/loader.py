import json

RAW_BOOK_FIELDS = (
    "title",
    "price",
    "availability",
    "rating",
    "book_url",
    "image_url",
)

CLEANED_BOOK_FIELDS = (
    "title",
    "price_gbp",
    "availability",
    "rating",
    "book_url",
    "image_url",
)

INSERT_RAW_BOOK_SQL = """
INSERT INTO raw_books (
    run_id,
    source_url,
    title,
    price,
    availability,
    rating,
    book_url,
    image_url,
    raw_payload
) VALUES (
    %(run_id)s,
    %(source_url)s,
    %(title)s,
    %(price)s,
    %(availability)s,
    %(rating)s,
    %(book_url)s,
    %(image_url)s,
    %(raw_payload)s::jsonb
);
"""

INSERT_CLEANED_BOOK_SQL = """
INSERT INTO cleaned_books (
    title,
    price_gbp,
    availability,
    rating,
    book_url,
    image_url,
    source_url
) VALUES (
    %(title)s,
    %(price_gbp)s,
    %(availability)s,
    %(rating)s,
    %(book_url)s,
    %(image_url)s,
    %(source_url)s
)
ON CONFLICT (book_url) DO UPDATE SET
    title = EXCLUDED.title,
    price_gbp = EXCLUDED.price_gbp,
    availability = EXCLUDED.availability,
    rating = EXCLUDED.rating,
    image_url = EXCLUDED.image_url,
    source_url = EXCLUDED.source_url,
    loaded_at = NOW();
"""


def insert_raw_books(connection, records, run_id, source_url):
    """Insert raw scraped book records and return the inserted row count."""
    if not run_id:
        raise ValueError("run_id is required")

    if not source_url:
        raise ValueError("source_url is required")

    inserted_count = 0

    with connection.cursor() as cursor:
        for record in records:
            cursor.execute(
                INSERT_RAW_BOOK_SQL,
                _build_raw_book_params(record, run_id, source_url),
            )
            inserted_count += 1

    return inserted_count


def insert_cleaned_books(connection, records, source_url):
    """Insert cleaned book records and update duplicates by book URL."""
    if not source_url:
        raise ValueError("source_url is required")

    rows = [_build_cleaned_book_params(record, source_url) for record in records]

    with connection.cursor() as cursor:
        for row in rows:
            cursor.execute(INSERT_CLEANED_BOOK_SQL, row)

    return len(rows)


def _build_raw_book_params(record, run_id, source_url):
    """Build SQL parameters for one raw book record."""
    params = {
        "run_id": run_id,
        "source_url": source_url,
        "raw_payload": json.dumps(record, sort_keys=True),
    }

    for field in RAW_BOOK_FIELDS:
        params[field] = record.get(field, "")

    return params


def _build_cleaned_book_params(record, source_url):
    """Build SQL parameters for one cleaned book record."""
    title = str(record.get("title", "") or "").strip()
    book_url = str(record.get("book_url", "") or "").strip()

    if not title:
        raise ValueError("title is required")

    if not book_url:
        raise ValueError("book_url is required")

    params = {
        "source_url": source_url,
        "price_gbp": _empty_to_none(record.get("price_gbp", "")),
        "rating": _empty_to_none(record.get("rating", "")),
    }

    for field in CLEANED_BOOK_FIELDS:
        if field not in params:
            params[field] = record.get(field, "")

    params["title"] = title
    params["book_url"] = book_url
    return params


def _empty_to_none(value):
    """Convert blank database values to NULL-friendly None."""
    if value == "":
        return None

    return value
