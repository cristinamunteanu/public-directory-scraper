from dataclasses import dataclass
from urllib.parse import urlparse
from urllib.request import Request, urlopen

DEFAULT_ALLOWED_SCHEMES = {"http", "https"}


@dataclass(frozen=True)
class FetchResult:
    """HTTP response details returned by fetch_url."""

    status_code: int
    reason: str
    body: bytes


def fetch_url(url, timeout=10, retries=0, allowed_schemes=DEFAULT_ALLOWED_SCHEMES):
    """Fetch one URL and return its status, reason, and response body."""
    if retries < 0:
        raise ValueError("retries must be at least 0")

    scheme = urlparse(url).scheme
    if scheme not in allowed_schemes:
        allowed = ", ".join(sorted(allowed_schemes))
        raise ValueError(f"URL scheme must be one of: {allowed}")

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
