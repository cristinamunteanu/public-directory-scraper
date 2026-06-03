from dataclasses import dataclass
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class FetchResult:
    """HTTP response details returned by fetch_url."""

    status_code: int
    reason: str
    body: bytes


def fetch_url(url, timeout=10):
    """Fetch one URL and return its status, reason, and response body."""
    request = Request(url, headers={"User-Agent": "public-directory-scraper/0.1"})

    with urlopen(request, timeout=timeout) as response:
        return FetchResult(
            status_code=getattr(response, "status", None) or 200,
            reason=getattr(response, "reason", None) or "OK",
            body=response.read(),
        )
