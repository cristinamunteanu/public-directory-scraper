from html.parser import HTMLParser
from urllib.parse import urljoin


class _BooksParser(HTMLParser):
    """Collect book records from Books to Scrape product_pod markup."""

    def __init__(self):
        """Prepare parser state for collecting book records."""
        super().__init__()
        self._current_book = None
        self._current_field = None
        self._field_depth = 0
        self._field_parts = []
        self.records = []

    def handle_starttag(self, tag, attrs):
        """Start collecting product fields from matching Books to Scrape tags."""
        attrs_by_name = dict(attrs)
        classes = attrs_by_name.get("class", "").split()

        if tag == "article" and "product_pod" in classes:
            self._current_book = {
                "title": "",
                "price": "",
                "availability": "",
                "rating": "",
                "book_url": "",
                "image_url": "",
            }
            return

        if self._current_book is None:
            return

        if tag == "img":
            self._current_book["image_url"] = attrs_by_name.get("src", "").strip()

        if tag == "a" and attrs_by_name.get("title"):
            self._current_book["title"] = attrs_by_name.get("title", "").strip()
            self._current_book["book_url"] = attrs_by_name.get("href", "").strip()

        if tag == "p" and "star-rating" in classes:
            self._current_book["rating"] = next(
                (class_name for class_name in classes if class_name != "star-rating"),
                "",
            )

        if tag == "p" and "price_color" in classes:
            self._start_field("price")
            return

        if tag == "p" and "availability" in classes:
            self._start_field("availability")
            return

        if self._current_field is not None:
            self._field_depth += 1

    def handle_data(self, data):
        """Collect text while inside price or availability fields."""
        if self._current_field is not None:
            self._field_parts.append(data)

    def handle_endtag(self, tag):
        """Finish product records and field text when their tags close."""
        if self._current_field is not None:
            self._field_depth -= 1
            if self._field_depth <= 0:
                self._finish_field()
            return

        if tag == "article":
            self._finish_book()

    def _start_field(self, field):
        """Start collecting text for a single book field."""
        self._current_field = field
        self._field_depth = 1
        self._field_parts = []

    def _finish_field(self):
        """Store the collected text for the active book field."""
        if self._current_book is not None:
            self._current_book[self._current_field] = _normalize_space(
                self._field_parts
            )

        self._current_field = None
        self._field_depth = 0
        self._field_parts = []

    def _finish_book(self):
        """Store the current book record if any field was collected."""
        if self._current_book is None:
            return

        if any(self._current_book.values()):
            self.records.append(self._current_book)

        self._current_book = None


class _NextPageParser(HTMLParser):
    """Find the href inside a Books to Scrape pagination next item."""

    def __init__(self):
        """Prepare parser state for finding one next-page link."""
        super().__init__()
        self._inside_next = False
        self.next_page_url = ""

    def handle_starttag(self, tag, attrs):
        """Capture the first link inside a next pagination list item."""
        attrs_by_name = dict(attrs)
        classes = attrs_by_name.get("class", "").split()

        if tag == "li" and "next" in classes:
            self._inside_next = True
            return

        if tag == "a" and self._inside_next and not self.next_page_url:
            self.next_page_url = attrs_by_name.get("href", "").strip()

    def handle_endtag(self, tag):
        """Leave next-link mode when the pagination list item closes."""
        if tag == "li" and self._inside_next:
            self._inside_next = False


def _normalize_space(parts):
    """Collapse whitespace from a list of text parts."""
    return " ".join(part.strip() for part in parts if part.strip())


def parse_listings(html):
    """Parse all Books to Scrape listing records."""
    book_records = _parse_books_listings(html)
    if book_records:
        return book_records

    raise ValueError("book listing must include title and book_url")


def _parse_books_listings(html):
    """Parse Books to Scrape records when product card markup is present."""
    parser = _BooksParser()
    parser.feed(html)
    parser.close()

    if not parser.records:
        return []

    if all(record["title"] and record["book_url"] for record in parser.records):
        return parser.records

    return []


def _parse_books(html):
    """Parse all Books to Scrape records from product_pod markup."""
    records = _parse_books_listings(html)

    if not records:
        raise ValueError("book listing must include title and book_url")

    return records


def parse_listing(html):
    """Parse HTML and return the first listing record."""
    return parse_listings(html)[0]


def parse_next_page_url(html, base_url):
    """Return the absolute next-page URL from Books pagination, if present."""
    parser = _NextPageParser()
    parser.feed(html)
    parser.close()

    if not parser.next_page_url:
        return ""

    return urljoin(base_url, parser.next_page_url)
