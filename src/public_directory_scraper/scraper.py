from .cleaner import clean_books_records
from .fetcher import fetch_url
from .parser import parse_listings


def scrape_url(url):
    """Fetch one URL, decode the response as HTML, and parse listing records."""
    result = fetch_url(url)
    html = result.body.decode("utf-8", errors="replace")
    records = parse_listings(html)

    if records and "title" in records[0]:
        return clean_books_records(records, base_url=url)

    return records
