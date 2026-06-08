import unittest
from unittest.mock import patch

from public_directory_scraper.fetcher import FetchResult
from public_directory_scraper.scraper import scrape_pages, scrape_url


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

    def test_passes_timeout_to_fetcher(self):
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

            scrape_url("https://example.com/directory", timeout=2.5)

        self.assertEqual(fetch_url.call_args.kwargs["timeout"], 2.5)

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

    def test_follows_next_links_up_to_page_limit(self):
        first_page = b"""
        <article class="product_pod">
          <p class="star-rating Three"></p>
          <h3>
            <a href="book_1/index.html" title="First Book">Book</a>
          </h3>
          <img src="media/cache/first.jpg">
          <p class="price_color">\xc2\xa351.77</p>
          <p class="instock availability">In stock</p>
        </article>
        <ul class="pager">
          <li class="next"><a href="page-2.html">next</a></li>
        </ul>
        """
        second_page = b"""
        <article class="product_pod">
          <p class="star-rating Four"></p>
          <h3>
            <a href="book_2/index.html" title="Second Book">Book</a>
          </h3>
          <img src="media/cache/second.jpg">
          <p class="price_color">\xc2\xa333.78</p>
          <p class="instock availability">In stock</p>
        </article>
        """

        with patch("public_directory_scraper.scraper.fetch_url") as fetch_url:
            fetch_url.side_effect = [
                FetchResult(status_code=200, reason="OK", body=first_page),
                FetchResult(status_code=200, reason="OK", body=second_page),
            ]

            records = scrape_pages(
                "https://books.toscrape.com/catalogue/page-1.html",
                max_pages=2,
            )

        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]["title"], "First Book")
        self.assertEqual(records[1]["title"], "Second Book")
        self.assertEqual(records[1]["rating"], 4)
        self.assertEqual(
            fetch_url.call_args_list[1].args[0],
            "https://books.toscrape.com/catalogue/page-2.html",
        )

    def test_waits_between_paginated_requests_when_delay_is_set(self):
        first_page = b"""
        <article class="product_pod">
          <p class="star-rating Three"></p>
          <h3>
            <a href="book_1/index.html" title="First Book">Book</a>
          </h3>
          <img src="media/cache/first.jpg">
          <p class="price_color">\xc2\xa351.77</p>
          <p class="instock availability">In stock</p>
        </article>
        <ul class="pager">
          <li class="next"><a href="page-2.html">next</a></li>
        </ul>
        """
        second_page = b"""
        <article class="product_pod">
          <p class="star-rating Four"></p>
          <h3>
            <a href="book_2/index.html" title="Second Book">Book</a>
          </h3>
          <img src="media/cache/second.jpg">
          <p class="price_color">\xc2\xa333.78</p>
          <p class="instock availability">In stock</p>
        </article>
        """

        with (
            patch("public_directory_scraper.scraper.fetch_url") as fetch_url,
            patch("public_directory_scraper.scraper.sleep") as sleep,
        ):
            fetch_url.side_effect = [
                FetchResult(status_code=200, reason="OK", body=first_page),
                FetchResult(status_code=200, reason="OK", body=second_page),
            ]

            records = scrape_pages(
                "https://books.toscrape.com/catalogue/page-1.html",
                max_pages=2,
                delay=1.5,
            )

        self.assertEqual(len(records), 2)
        self.assertEqual(sleep.call_args.args[0], 1.5)
        self.assertEqual(sleep.call_count, 1)

    def test_removes_duplicate_books_across_pages(self):
        first_page = b"""
        <article class="product_pod">
          <p class="star-rating Three"></p>
          <h3>
            <a href="book_1/index.html" title="First Book">Book</a>
          </h3>
          <img src="media/cache/first.jpg">
          <p class="price_color">\xc2\xa351.77</p>
          <p class="instock availability">In stock</p>
        </article>
        <ul class="pager">
          <li class="next"><a href="page-2.html">next</a></li>
        </ul>
        """
        second_page = b"""
        <article class="product_pod">
          <p class="star-rating Four"></p>
          <h3>
            <a href="book_1/index.html" title="Duplicate Book">Book</a>
          </h3>
          <img src="media/cache/duplicate.jpg">
          <p class="price_color">\xc2\xa333.78</p>
          <p class="instock availability">In stock</p>
        </article>
        """

        with patch("public_directory_scraper.scraper.fetch_url") as fetch_url:
            fetch_url.side_effect = [
                FetchResult(status_code=200, reason="OK", body=first_page),
                FetchResult(status_code=200, reason="OK", body=second_page),
            ]

            records = scrape_pages(
                "https://books.toscrape.com/catalogue/page-1.html",
                max_pages=2,
            )

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["title"], "First Book")

    def test_rejects_page_limit_below_one(self):
        with self.assertRaisesRegex(ValueError, "pages must be at least 1"):
            scrape_pages("https://books.toscrape.com/", max_pages=0)

    def test_rejects_negative_delay(self):
        with self.assertRaisesRegex(ValueError, "delay must be at least 0"):
            scrape_pages("https://books.toscrape.com/", delay=-1)


if __name__ == "__main__":
    unittest.main()
