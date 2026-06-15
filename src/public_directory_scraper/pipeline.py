from dataclasses import dataclass

from .cleaner import clean_books_records, deduplicate_records
from .loader import insert_cleaned_books, insert_raw_books
from .scraper import extract_books_pages


@dataclass(frozen=True)
class EtlResult:
    """Summary counts from one ETL load."""

    raw_count: int
    cleaned_count: int


def load_books_records(connection, records, run_id, source_url):
    """Load raw book records, clean them, and load cleaned records."""
    try:
        raw_count = insert_raw_books(
            connection,
            records,
            run_id=run_id,
            source_url=source_url,
        )
        cleaned_records = deduplicate_records(
            clean_books_records(records, base_url=source_url),
            key="book_url",
        )
        cleaned_count = insert_cleaned_books(
            connection,
            cleaned_records,
            source_url=source_url,
        )
        connection.commit()
    except Exception:
        _rollback_if_available(connection)
        raise

    return EtlResult(raw_count=raw_count, cleaned_count=cleaned_count)


def run_books_etl(
    connection,
    url,
    run_id,
    pages=1,
    timeout=10,
    delay=0,
    retries=0,
):
    """Extract raw book records from pages and load them into Postgres tables."""
    records = extract_books_pages(
        url,
        max_pages=pages,
        timeout=timeout,
        delay=delay,
        retries=retries,
    )

    return load_books_records(
        connection,
        records,
        run_id=run_id,
        source_url=url,
    )


def _rollback_if_available(connection):
    """Rollback the active transaction when the connection supports it."""
    rollback = getattr(connection, "rollback", None)

    if rollback is not None:
        rollback()
