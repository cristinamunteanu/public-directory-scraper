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


if __name__ == "__main__":
    unittest.main()
