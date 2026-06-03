from .fetcher import fetch_url
from .parser import parse_listings


def scrape_url(url):
    result = fetch_url(url)
    html = result.body.decode("utf-8", errors="replace")
    return parse_listings(html)
