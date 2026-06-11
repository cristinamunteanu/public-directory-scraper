from dataclasses import dataclass

from .cleaner import clean_books_records, deduplicate_records
from .loader import insert_cleaned_books, insert_raw_books


@dataclass(frozen=True)
class EtlResult:
    """Summary counts from one ETL load."""

    raw_count: int
    cleaned_count: int


def load_books_records(connection, records, run_id, source_url):
    """Load raw book records, clean them, and load cleaned records."""
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

    return EtlResult(raw_count=raw_count, cleaned_count=cleaned_count)
