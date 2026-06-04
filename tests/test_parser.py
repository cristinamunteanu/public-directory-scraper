import unittest
from pathlib import Path

from public_directory_scraper.parser import parse_listing, parse_listings

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


class ParseListingTest(unittest.TestCase):
    def test_parses_simple_listing(self):
        html = (FIXTURES_DIR / "simple_listing.html").read_text(encoding="utf-8")

        record = parse_listing(html)

        self.assertEqual(
            record,
            {
                "name": "Example Business",
                "url": "https://example.com",
            },
        )

    def test_parses_multiple_listings(self):
        html = (FIXTURES_DIR / "listings.html").read_text(encoding="utf-8")

        records = parse_listings(html)

        self.assertEqual(
            records,
            [
                {
                    "name": "Example Business",
                    "url": "https://example.com",
                },
                {
                    "name": "Second Business",
                    "url": "https://second.example",
                },
            ],
        )

    def test_parses_books_to_scrape_page(self):
        html = (FIXTURES_DIR / "books_page.html").read_text(encoding="utf-8")

        records = parse_listings(html)

        self.assertEqual(
            records,
            [
                {
                    "title": "A Light in the Attic",
                    "price": "£51.77",
                    "availability": "In stock",
                    "rating": "Three",
                    "book_url": "catalogue/a-light-in-the-attic_1000/index.html",
                    "image_url": (
                        "media/cache/2c/da/"
                        "2cdad67c44b002e7ead0cc35693c0e8b.jpg"
                    ),
                },
                {
                    "title": "Tipping the Velvet",
                    "price": "£53.74",
                    "availability": "In stock",
                    "rating": "One",
                    "book_url": "catalogue/tipping-the-velvet_999/index.html",
                    "image_url": (
                        "media/cache/26/0c/"
                        "260c6ae16bce31c8f8c95dadd11e0f83.jpg"
                    ),
                },
            ],
        )

    def test_requires_name_and_url(self):
        with self.assertRaisesRegex(ValueError, "listing must include name and url"):
            parse_listings("<article></article>")


if __name__ == "__main__":
    unittest.main()
