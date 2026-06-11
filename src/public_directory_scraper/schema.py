CREATE_RAW_BOOKS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS raw_books (
    id BIGSERIAL PRIMARY KEY,
    run_id TEXT NOT NULL,
    source_url TEXT NOT NULL,
    title TEXT,
    price TEXT,
    availability TEXT,
    rating TEXT,
    book_url TEXT,
    image_url TEXT,
    raw_payload JSONB NOT NULL,
    extracted_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""

CREATE_CLEANED_BOOKS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS cleaned_books (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    price_gbp NUMERIC,
    availability TEXT,
    rating INTEGER,
    book_url TEXT NOT NULL UNIQUE,
    image_url TEXT,
    source_url TEXT NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""


def create_tables(connection):
    """Create raw and cleaned book tables if they do not already exist."""
    with connection.cursor() as cursor:
        cursor.execute(CREATE_RAW_BOOKS_TABLE_SQL)
        cursor.execute(CREATE_CLEANED_BOOKS_TABLE_SQL)

    connection.commit()
