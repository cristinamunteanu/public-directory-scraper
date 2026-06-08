from dataclasses import dataclass
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class FetchResult:
    """HTTP response details returned by fetch_url."""

    status_code: int
    reason: str
    body: bytes


def fetch_url(url, timeout=10, retries=0):
    """Fetch one URL and return its status, reason, and response body."""
    if retries < 0:
        raise ValueError("retries must be at least 0")

    request = Request(url, headers={"User-Agent": "public-directory-scraper/0.1"})

    for attempt in range(retries + 1):
        try:
            with urlopen(request, timeout=timeout) as response:
                return FetchResult(
                    status_code=getattr(response, "status", None) or 200,
                    reason=getattr(response, "reason", None) or "OK",
                    body=response.read(),
                )
        except OSError:
            if attempt == retries:
                raise

    raise RuntimeError("unreachable fetch retry state")
