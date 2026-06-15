import os
import unittest

from public_directory_scraper.database import connect
from public_directory_scraper.pipeline import EtlResult, load_books_records
from public_directory_scraper.schema import create_tables

INTEGRATION_DATABASE_URL = os.environ.get("INTEGRATION_DATABASE_URL", "")


@unittest.skipUnless(
    INTEGRATION_DATABASE_URL,
    "set INTEGRATION_DATABASE_URL to run Postgres integration tests",
)
class PostgresIntegrationTest(unittest.TestCase):
    def test_loads_raw_and_cleaned_books_in_postgres(self):
        connection = connect(INTEGRATION_DATABASE_URL)
        run_id = "integration-test-run"
        book_url = "integration-test-book/index.html"
        cleaned_book_url = f"https://books.toscrape.com/{book_url}"

        try:
            create_tables(connection)
            _delete_test_rows(connection, run_id, cleaned_book_url)

            result = load_books_records(
                connection,
                [
                    {
                        "title": "Integration Test Book",
                        "price": "£10.50",
                        "availability": "In stock",
                        "rating": "Two",
                        "book_url": book_url,
                        "image_url": "media/cache/integration-test.jpg",
                    }
                ],
                run_id=run_id,
                source_url="https://books.toscrape.com/",
            )

            self.assertEqual(
                result,
                EtlResult(run_id=run_id, raw_count=1, cleaned_count=1),
            )
            self.assertEqual(_count_raw_rows(connection, run_id), 1)
            self.assertEqual(_count_cleaned_rows(connection, cleaned_book_url), 1)
        finally:
            _delete_test_rows(connection, run_id, cleaned_book_url)
            connection.close()


def _count_raw_rows(connection, run_id):
    """Count raw rows for the integration test run."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM raw_books WHERE run_id = %s", [run_id])
        return cursor.fetchone()[0]


def _count_cleaned_rows(connection, book_url):
    """Count cleaned rows for the integration test book URL."""
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT COUNT(*) FROM cleaned_books WHERE book_url = %s",
            [book_url],
        )
        return cursor.fetchone()[0]


def _delete_test_rows(connection, run_id, book_url):
    """Delete rows created by the integration test."""
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM raw_books WHERE run_id = %s", [run_id])
        cursor.execute("DELETE FROM cleaned_books WHERE book_url = %s", [book_url])

    connection.commit()


if __name__ == "__main__":
    unittest.main()
