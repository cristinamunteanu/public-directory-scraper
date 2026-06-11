import json

RAW_BOOK_FIELDS = (
    "title",
    "price",
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

    connection.commit()
    return inserted_count


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
