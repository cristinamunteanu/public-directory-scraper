from .fetcher import fetch_url
from .parser import parse_listings


def scrape_url(url):
    """Fetch one URL, decode the response as HTML, and parse listing records."""
    result = fetch_url(url)
    html = result.body.decode("utf-8", errors="replace")
    return parse_listings(html)
