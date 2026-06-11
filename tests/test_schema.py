import unittest

from public_directory_scraper.schema import (
    CREATE_CLEANED_BOOKS_TABLE_SQL,
    CREATE_RAW_BOOKS_TABLE_SQL,
    create_tables,
)


class FakeCursor:
    def __init__(self):
        self.statements = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return None

    def execute(self, statement):
        self.statements.append(statement)


class FakeConnection:
    def __init__(self):
        self.cursor_instance = FakeCursor()
        self.committed = False

    def cursor(self):
        return self.cursor_instance

    def commit(self):
        self.committed = True


class CreateTablesTest(unittest.TestCase):
    def test_creates_raw_and_cleaned_book_tables(self):
        connection = FakeConnection()

        create_tables(connection)

        self.assertEqual(
            connection.cursor_instance.statements,
            [
                CREATE_RAW_BOOKS_TABLE_SQL,
                CREATE_CLEANED_BOOKS_TABLE_SQL,
            ],
        )
        self.assertTrue(connection.committed)

    def test_cleaned_books_are_unique_by_book_url(self):
        self.assertIn("book_url TEXT NOT NULL UNIQUE", CREATE_CLEANED_BOOKS_TABLE_SQL)

    def test_raw_books_store_original_payload(self):
        self.assertIn("raw_payload JSONB NOT NULL", CREATE_RAW_BOOKS_TABLE_SQL)


if __name__ == "__main__":
    unittest.main()
