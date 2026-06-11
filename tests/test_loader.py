import json
import unittest

from public_directory_scraper.loader import INSERT_RAW_BOOK_SQL, insert_raw_books


class FakeCursor:
    def __init__(self):
        self.calls = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return None

    def execute(self, statement, params):
        self.calls.append((statement, params))


class FakeConnection:
    def __init__(self):
        self.cursor_instance = FakeCursor()
        self.committed = False

    def cursor(self):
        return self.cursor_instance

    def commit(self):
        self.committed = True


class InsertRawBooksTest(unittest.TestCase):
    def test_inserts_raw_book_records(self):
        connection = FakeConnection()
        record = {
            "title": "A Light in the Attic",
            "price": "£51.77",
            "availability": "In stock",
            "rating": "Three",
            "book_url": "catalogue/a-light-in-the-attic_1000/index.html",
            "image_url": "media/cache/book.jpg",
        }

        inserted_count = insert_raw_books(
            connection,
            [record],
            run_id="run-1",
            source_url="https://books.toscrape.com/",
        )

        self.assertEqual(inserted_count, 1)
        self.assertTrue(connection.committed)

        statement, params = connection.cursor_instance.calls[0]
        self.assertEqual(statement, INSERT_RAW_BOOK_SQL)
        self.assertEqual(params["run_id"], "run-1")
        self.assertEqual(params["source_url"], "https://books.toscrape.com/")
        self.assertEqual(params["title"], "A Light in the Attic")
        self.assertEqual(params["price"], "£51.77")
        self.assertEqual(params["availability"], "In stock")
        self.assertEqual(params["rating"], "Three")
        self.assertEqual(
            params["book_url"],
            "catalogue/a-light-in-the-attic_1000/index.html",
        )
        self.assertEqual(params["image_url"], "media/cache/book.jpg")
        self.assertEqual(params["raw_payload"], json.dumps(record, sort_keys=True))

    def test_fills_missing_raw_fields_with_empty_strings(self):
        connection = FakeConnection()

        inserted_count = insert_raw_books(
            connection,
            [{"title": "Incomplete Book"}],
            run_id="run-1",
            source_url="https://books.toscrape.com/",
        )

        self.assertEqual(inserted_count, 1)

        params = connection.cursor_instance.calls[0][1]
        self.assertEqual(params["title"], "Incomplete Book")
        self.assertEqual(params["price"], "")
        self.assertEqual(params["availability"], "")
        self.assertEqual(params["rating"], "")
        self.assertEqual(params["book_url"], "")
        self.assertEqual(params["image_url"], "")
        self.assertEqual(
            params["raw_payload"],
            json.dumps({"title": "Incomplete Book"}, sort_keys=True),
        )

    def test_requires_run_id(self):
        with self.assertRaisesRegex(ValueError, "run_id is required"):
            insert_raw_books(
                FakeConnection(),
                [],
                run_id="",
                source_url="https://books.toscrape.com/",
            )

    def test_requires_source_url(self):
        with self.assertRaisesRegex(ValueError, "source_url is required"):
            insert_raw_books(FakeConnection(), [], run_id="run-1", source_url="")


if __name__ == "__main__":
    unittest.main()
