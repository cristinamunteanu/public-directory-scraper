import unittest
from unittest.mock import patch

from public_directory_scraper.pipeline import (
    EtlResult,
    load_books_records,
    run_books_etl,
)


class LoadBooksRecordsTest(unittest.TestCase):
    def test_loads_raw_then_cleaned_records(self):
        connection = FakeConnection()
        records = [
            {
                "title": "A Light in the Attic",
                "price": "£51.77",
                "availability": "In stock",
                "rating": "Three",
                "book_url": "catalogue/a-light-in-the-attic_1000/index.html",
                "image_url": "media/cache/book.jpg",
            },
            {
                "title": "Duplicate Book",
                "price": "£51.77",
                "availability": "In stock",
                "rating": "Three",
                "book_url": "catalogue/a-light-in-the-attic_1000/index.html",
                "image_url": "media/cache/book.jpg",
            },
        ]

        with (
            patch("public_directory_scraper.pipeline.insert_raw_books") as raw_loader,
            patch(
                "public_directory_scraper.pipeline.insert_cleaned_books"
            ) as cleaned_loader,
        ):
            raw_loader.return_value = 2
            cleaned_loader.return_value = 1

            result = load_books_records(
                connection,
                records,
                run_id="run-1",
                source_url="https://books.toscrape.com/",
            )

        self.assertEqual(
            result,
            EtlResult(run_id="run-1", raw_count=2, cleaned_count=1),
        )
        raw_loader.assert_called_once_with(
            connection,
            records,
            run_id="run-1",
            source_url="https://books.toscrape.com/",
        )

        cleaned_records = cleaned_loader.call_args.args[1]
        self.assertEqual(
            cleaned_loader.call_args.kwargs["source_url"],
            "https://books.toscrape.com/",
        )
        self.assertEqual(len(cleaned_records), 1)
        self.assertEqual(cleaned_records[0]["title"], "A Light in the Attic")
        self.assertEqual(cleaned_records[0]["price_gbp"], 51.77)
        self.assertEqual(cleaned_records[0]["rating"], 3)
        self.assertEqual(
            cleaned_records[0]["book_url"],
            "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
        )
        self.assertFalse(connection.rolled_back)
        self.assertTrue(connection.committed)

    def test_rolls_back_when_cleaned_load_fails(self):
        connection = FakeConnection()
        records = [
            {
                "title": "A Light in the Attic",
                "price": "£51.77",
                "availability": "In stock",
                "rating": "Three",
                "book_url": "catalogue/a-light-in-the-attic_1000/index.html",
                "image_url": "media/cache/book.jpg",
            }
        ]

        with (
            patch("public_directory_scraper.pipeline.insert_raw_books") as raw_loader,
            patch(
                "public_directory_scraper.pipeline.insert_cleaned_books"
            ) as cleaned_loader,
        ):
            raw_loader.return_value = 1
            cleaned_loader.side_effect = RuntimeError("cleaned load failed")

            with self.assertRaisesRegex(RuntimeError, "cleaned load failed"):
                load_books_records(
                    connection,
                    records,
                    run_id="run-1",
                    source_url="https://books.toscrape.com/",
                )

        self.assertFalse(connection.committed)
        self.assertTrue(connection.rolled_back)


class RunBooksEtlTest(unittest.TestCase):
    def test_extracts_pages_then_loads_records(self):
        connection = object()
        records = [
            {
                "title": "A Light in the Attic",
                "price": "£51.77",
                "availability": "In stock",
                "rating": "Three",
                "book_url": "catalogue/a-light-in-the-attic_1000/index.html",
                "image_url": "media/cache/book.jpg",
            }
        ]

        with (
            patch(
                "public_directory_scraper.pipeline.extract_books_pages"
            ) as extract_pages,
            patch("public_directory_scraper.pipeline.load_books_records") as load,
        ):
            extract_pages.return_value = records
            load.return_value = EtlResult(
                run_id="run-1",
                raw_count=1,
                cleaned_count=1,
            )

            result = run_books_etl(
                connection,
                "https://books.toscrape.com/",
                run_id="run-1",
                pages=2,
                timeout=5,
                delay=1,
                retries=1,
            )

        self.assertEqual(
            result,
            EtlResult(run_id="run-1", raw_count=1, cleaned_count=1),
        )
        extract_pages.assert_called_once_with(
            "https://books.toscrape.com/",
            max_pages=2,
            timeout=5,
            delay=1,
            retries=1,
        )
        load.assert_called_once_with(
            connection,
            records,
            run_id="run-1",
            source_url="https://books.toscrape.com/",
        )


class FakeConnection:
    def __init__(self):
        self.committed = False
        self.rolled_back = False

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True


if __name__ == "__main__":
    unittest.main()
