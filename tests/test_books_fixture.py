import unittest
from pathlib import Path

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


class BooksFixtureTest(unittest.TestCase):
    def test_books_fixture_has_representative_page_structure(self):
        html = (FIXTURES_DIR / "books_page.html").read_text(encoding="utf-8")

        self.assertEqual(html.count('class="product_pod"'), 2)
        self.assertIn('class="price_color"', html)
        self.assertIn('class="instock availability"', html)
        self.assertIn('class="star-rating Three"', html)
        self.assertIn('title="A Light in the Attic"', html)
        self.assertIn('href="catalogue/page-2.html"', html)


if __name__ == "__main__":
    unittest.main()
