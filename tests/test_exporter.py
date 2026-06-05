import csv
import tempfile
import unittest
from pathlib import Path

from public_directory_scraper.exporter import write_records_csv


class WriteRecordsCsvTest(unittest.TestCase):
    def test_writes_records_to_csv(self):
        records = [
            {"name": "Example Business", "url": "https://example.com"},
            {"name": "Second Business", "url": "https://second.example"},
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "listings.csv"

            count = write_records_csv(records, output_path)

            with output_path.open(encoding="utf-8", newline="") as csv_file:
                rows = list(csv.DictReader(csv_file))

        self.assertEqual(count, 2)
        self.assertEqual(rows, records)

    def test_writes_books_records_to_csv(self):
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

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "books.csv"

            count = write_records_csv(records, output_path)

            with output_path.open(encoding="utf-8", newline="") as csv_file:
                reader = csv.DictReader(csv_file)
                fieldnames = reader.fieldnames
                rows = list(reader)

        self.assertEqual(count, 1)
        self.assertEqual(
            fieldnames,
            ["title", "price", "availability", "rating", "book_url", "image_url"],
        )
        self.assertEqual(rows, records)


if __name__ == "__main__":
    unittest.main()
