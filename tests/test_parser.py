import unittest
from pathlib import Path

from public_directory_scraper.parser import parse_listing


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

    def test_requires_name_and_url(self):
        with self.assertRaisesRegex(ValueError, "listing must include name and url"):
            parse_listing("<article></article>")


if __name__ == "__main__":
    unittest.main()
