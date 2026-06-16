import unittest

from public_directory_scraper.parser import (
    parse_listing,
    parse_listings,
    parse_next_page_url,
)

BOOKS_HTML = """
<article class="product_pod">
  <p class="star-rating Three"></p>
  <h3>
    <a
      href="catalogue/a-light-in-the-attic_1000/index.html"
      title="A Light in the Attic"
    >Book</a>
  </h3>
  <img src="media/cache/book.jpg">
  <p class="price_color">£51.77</p>
  <p class="instock availability">In stock</p>
</article>
<article class="product_pod">
  <p class="star-rating One"></p>
  <h3>
    <a
      href="catalogue/tipping-the-velvet_999/index.html"
      title="Tipping the Velvet"
    >Book</a>
  </h3>
  <img src="media/cache/second.jpg">
  <p class="price_color">£53.74</p>
  <p class="instock availability">In stock</p>
</article>
<ul class="pager">
  <li class="next"><a href="catalogue/page-2.html">next</a></li>
</ul>
"""


class ParseListingTest(unittest.TestCase):
    def test_parses_first_books_to_scrape_listing(self):
        record = parse_listing(BOOKS_HTML)

        self.assertEqual(
            record,
            {
                "title": "A Light in the Attic",
                "price": "£51.77",
                "availability": "In stock",
                "rating": "Three",
                "book_url": "catalogue/a-light-in-the-attic_1000/index.html",
                "image_url": "media/cache/book.jpg",
            },
        )

    def test_parses_books_to_scrape_page(self):
        records = parse_listings(BOOKS_HTML)

        self.assertEqual(
            records,
            [
                {
                    "title": "A Light in the Attic",
                    "price": "£51.77",
                    "availability": "In stock",
                    "rating": "Three",
                    "book_url": "catalogue/a-light-in-the-attic_1000/index.html",
                    "image_url": "media/cache/book.jpg",
                },
                {
                    "title": "Tipping the Velvet",
                    "price": "£53.74",
                    "availability": "In stock",
                    "rating": "One",
                    "book_url": "catalogue/tipping-the-velvet_999/index.html",
                    "image_url": "media/cache/second.jpg",
                },
            ],
        )

    def test_parses_books_next_page_url(self):
        next_page_url = parse_next_page_url(
            BOOKS_HTML,
            "https://books.toscrape.com/index.html",
        )

        self.assertEqual(
            next_page_url,
            "https://books.toscrape.com/catalogue/page-2.html",
        )

    def test_returns_empty_next_page_url_without_next_link(self):
        html = """
        <article class="product_pod">
          <p class="star-rating Four"></p>
          <h3><a href="book.html" title="Book">Book</a></h3>
        </article>
        """

        self.assertEqual(parse_next_page_url(html, "https://books.toscrape.com/"), "")

    def test_requires_books_markup(self):
        with self.assertRaisesRegex(
            ValueError,
            "book listing must include title and book_url",
        ):
            parse_listings("<article></article>")


if __name__ == "__main__":
    unittest.main()
