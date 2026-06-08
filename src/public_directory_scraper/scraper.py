from time import sleep

from .cleaner import clean_books_records, deduplicate_records
from .fetcher import fetch_url
from .parser import parse_listings, parse_next_page_url


def scrape_url(url, timeout=10, delay=0, retries=0):
    """Fetch one URL, decode the response as HTML, and parse listing records."""
    return scrape_pages(url, max_pages=1, timeout=timeout, delay=delay, retries=retries)


def scrape_pages(url, max_pages=1, timeout=10, delay=0, retries=0):
    """Fetch and parse pages by following next links up to max_pages."""
    if max_pages < 1:
        raise ValueError("pages must be at least 1")

    if delay < 0:
        raise ValueError("delay must be at least 0")

    records = []
    current_url = url

    for _page_number in range(max_pages):
        result = fetch_url(current_url, timeout=timeout, retries=retries)
        html = result.body.decode("utf-8", errors="replace")
        page_records = parse_listings(html)

        if page_records and "title" in page_records[0]:
            records.extend(clean_books_records(page_records, base_url=current_url))
        else:
            records.extend(page_records)

        next_url = parse_next_page_url(html, current_url)
        if not next_url:
            break

        if delay:
            sleep(delay)

        current_url = next_url

    return deduplicate_records(records, key="book_url")
