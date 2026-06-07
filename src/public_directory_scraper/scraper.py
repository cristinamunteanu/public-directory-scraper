from .cleaner import clean_books_records
from .fetcher import fetch_url
from .parser import parse_listings, parse_next_page_url


def scrape_url(url):
    """Fetch one URL, decode the response as HTML, and parse listing records."""
    return scrape_pages(url, max_pages=1)


def scrape_pages(url, max_pages=1):
    """Fetch and parse pages by following next links up to max_pages."""
    if max_pages < 1:
        raise ValueError("pages must be at least 1")

    records = []
    current_url = url

    for _page_number in range(max_pages):
        result = fetch_url(current_url)
        html = result.body.decode("utf-8", errors="replace")
        page_records = parse_listings(html)

        if page_records and "title" in page_records[0]:
            records.extend(clean_books_records(page_records, base_url=current_url))
        else:
            records.extend(page_records)

        next_url = parse_next_page_url(html, current_url)
        if not next_url:
            break

        current_url = next_url

    return records
