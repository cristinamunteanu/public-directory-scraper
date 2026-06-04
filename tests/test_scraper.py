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

    def test_fetches_parses_and_cleans_books(self):
        body = b"""
        <article class="product_pod">
          <p class="star-rating Three"></p>
          <h3>
            <a href="catalogue/book_1/index.html" title="Example Book">Book</a>
          </h3>
          <img src="media/cache/book.jpg">
          <p class="price_color">\xc2\xa351.77</p>
          <p class="instock availability">In stock</p>
        </article>
        """

        with patch("public_directory_scraper.scraper.fetch_url") as fetch_url:
            fetch_url.return_value = FetchResult(
                status_code=200,
                reason="OK",
                body=body,
            )

            records = scrape_url("https://books.toscrape.com/")

        self.assertEqual(
            records,
            [
                {
                    "title": "Example Book",
                    "price_gbp": 51.77,
                    "availability": "In stock",
                    "rating": 3,
                    "book_url": (
                        "https://books.toscrape.com/catalogue/book_1/index.html"
                    ),
                    "image_url": "https://books.toscrape.com/media/cache/book.jpg",
                },
            ],
        )


if __name__ == "__main__":
    unittest.main()
