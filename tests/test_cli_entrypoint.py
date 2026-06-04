import csv
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIXTURES_DIR = PROJECT_ROOT / "tests" / "fixtures"


class CliEntrypointTest(unittest.TestCase):
    def test_package_runs_as_module(self):
        env = os.environ.copy()
        env["PYTHONPATH"] = str(PROJECT_ROOT / "src")

        result = subprocess.run(
            [sys.executable, "-m", "public_directory_scraper"],
            check=True,
            capture_output=True,
            env=env,
            text=True,
        )

        self.assertEqual(result.stdout.strip(), "public-directory-scraper 0.1.0")
        self.assertEqual(result.stderr, "")

    def test_parse_command_prints_listing_json(self):
        env = os.environ.copy()
        env["PYTHONPATH"] = str(PROJECT_ROOT / "src")

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "public_directory_scraper",
                "parse",
                str(FIXTURES_DIR / "listings.html"),
            ],
            check=True,
            capture_output=True,
            env=env,
            text=True,
        )

        self.assertEqual(
            json.loads(result.stdout),
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
        self.assertEqual(result.stderr, "")

    def test_parse_command_prints_books_json(self):
        env = os.environ.copy()
        env["PYTHONPATH"] = str(PROJECT_ROOT / "src")

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "public_directory_scraper",
                "parse",
                str(FIXTURES_DIR / "books_page.html"),
            ],
            check=True,
            capture_output=True,
            env=env,
            text=True,
        )

        self.assertEqual(
            json.loads(result.stdout),
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
        self.assertEqual(result.stderr, "")

    def test_fetch_command_prints_status_and_bytes(self):
        env = os.environ.copy()
        env["PYTHONPATH"] = str(PROJECT_ROOT / "src")

        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "page.html"
            input_path.write_text("hello", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "public_directory_scraper",
                    "fetch",
                    input_path.as_uri(),
                ],
                check=True,
                capture_output=True,
                env=env,
                text=True,
            )

        self.assertEqual(result.stdout, "200 OK\nbytes: 5\n")
        self.assertEqual(result.stderr, "")

    def test_scrape_command_prints_listing_json(self):
        env = os.environ.copy()
        env["PYTHONPATH"] = str(PROJECT_ROOT / "src")

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "public_directory_scraper",
                "scrape",
                (FIXTURES_DIR / "listings.html").as_uri(),
            ],
            check=True,
            capture_output=True,
            env=env,
            text=True,
        )

        self.assertEqual(
            json.loads(result.stdout),
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
        self.assertEqual(result.stderr, "")

    def test_parse_command_writes_listing_csv(self):
        env = os.environ.copy()
        env["PYTHONPATH"] = str(PROJECT_ROOT / "src")

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "listings.csv"

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "public_directory_scraper",
                    "parse",
                    str(FIXTURES_DIR / "listings.html"),
                    "--output",
                    str(output_path),
                ],
                check=True,
                capture_output=True,
                env=env,
                text=True,
            )

            with output_path.open(encoding="utf-8", newline="") as csv_file:
                rows = list(csv.DictReader(csv_file))

        self.assertEqual(result.stdout.strip(), f"Wrote 2 records to {output_path}")
        self.assertEqual(result.stderr, "")
        self.assertEqual(
            rows,
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

    def test_parse_command_reports_missing_file(self):
        env = os.environ.copy()
        env["PYTHONPATH"] = str(PROJECT_ROOT / "src")
        missing_path = FIXTURES_DIR / "missing.html"

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "public_directory_scraper",
                "parse",
                str(missing_path),
            ],
            capture_output=True,
            env=env,
            text=True,
        )

        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertEqual(
            result.stderr.strip(),
            f"Error: file not found: {missing_path}",
        )

    def test_parse_command_reports_invalid_listing_html(self):
        env = os.environ.copy()
        env["PYTHONPATH"] = str(PROJECT_ROOT / "src")

        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "empty.html"
            input_path.write_text("<article></article>", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "public_directory_scraper",
                    "parse",
                    str(input_path),
                ],
                capture_output=True,
                env=env,
                text=True,
            )

        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertEqual(
            result.stderr.strip(),
            "Error: listing must include name and url",
        )


if __name__ == "__main__":
    unittest.main()
