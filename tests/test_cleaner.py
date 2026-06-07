import unittest

from public_directory_scraper.cleaner import clean_books_records, deduplicate_records


class CleanBooksRecordsTest(unittest.TestCase):
    def test_cleans_books_records(self):
        records = [
            {
                "title": " A Light in the Attic ",
                "price": "£51.77",
                "availability": "\n In stock \n",
                "rating": "Three",
                "book_url": "catalogue/a-light-in-the-attic_1000/index.html",
                "image_url": "media/cache/book.jpg",
            }
        ]

        cleaned = clean_books_records(records, base_url="https://books.toscrape.com/")

        self.assertEqual(
            cleaned,
            [
                {
                    "title": "A Light in the Attic",
                    "price_gbp": 51.77,
                    "availability": "In stock",
                    "rating": 3,
                    "book_url": (
                        "https://books.toscrape.com/catalogue/"
                        "a-light-in-the-attic_1000/index.html"
                    ),
                    "image_url": "https://books.toscrape.com/media/cache/book.jpg",
                }
            ],
        )

    def test_handles_missing_values(self):
        cleaned = clean_books_records([{}])

        self.assertEqual(
            cleaned,
            [
                {
                    "title": "",
                    "price_gbp": "",
                    "availability": "",
                    "rating": "",
                    "book_url": "https://books.toscrape.com/",
                    "image_url": "https://books.toscrape.com/",
                }
            ],
        )


class DeduplicateRecordsTest(unittest.TestCase):
    def test_removes_duplicate_records_by_key(self):
        records = [
            {"title": "First", "book_url": "https://example.com/book"},
            {"title": "Duplicate", "book_url": "https://example.com/book"},
            {"title": "Second", "book_url": "https://example.com/second"},
        ]

        self.assertEqual(
            deduplicate_records(records, key="book_url"),
            [
                {"title": "First", "book_url": "https://example.com/book"},
                {"title": "Second", "book_url": "https://example.com/second"},
            ],
        )

    def test_keeps_records_with_missing_key_values(self):
        records = [
            {"title": "Missing"},
            {"title": "Empty", "book_url": ""},
        ]

        self.assertEqual(deduplicate_records(records, key="book_url"), records)


if __name__ == "__main__":
    unittest.main()
