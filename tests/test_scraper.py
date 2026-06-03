import unittest
from unittest.mock import patch

from public_directory_scraper.fetcher import FetchResult
from public_directory_scraper.scraper import scrape_url


class ScrapeUrlTest(unittest.TestCase):
    def test_fetches_and_parses_listings(self):
        body = b"""
        <article>
          <h2 data-field="name">Example Business</h2>
          <a data-field="url" href="https://example.com">Visit website</a>
        </article>
        """

        with patch("public_directory_scraper.scraper.fetch_url") as fetch_url:
            fetch_url.return_value = FetchResult(
                status_code=200,
                reason="OK",
                body=body,
            )

            records = scrape_url("https://example.com/directory")

        self.assertEqual(
            records,
            [
                {
                    "name": "Example Business",
                    "url": "https://example.com",
                },
            ],
        )
        self.assertEqual(fetch_url.call_args.args[0], "https://example.com/directory")


if __name__ == "__main__":
    unittest.main()
