import unittest
from unittest.mock import patch

from public_directory_scraper.pipeline import EtlResult, load_books_records


class LoadBooksRecordsTest(unittest.TestCase):
    def test_loads_raw_then_cleaned_records(self):
        connection = object()
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

        self.assertEqual(result, EtlResult(raw_count=2, cleaned_count=1))
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


if __name__ == "__main__":
    unittest.main()
