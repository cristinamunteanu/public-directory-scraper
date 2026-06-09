import unittest
from unittest.mock import patch

from public_directory_scraper.fetcher import FetchResult, fetch_url


class FakeResponse:
    status = 200
    reason = "OK"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return None

    def read(self):
        return b"<html>hello</html>"


class FetchUrlTest(unittest.TestCase):
    def test_fetches_url_body_and_status(self):
        with patch("public_directory_scraper.fetcher.urlopen") as urlopen:
            urlopen.return_value = FakeResponse()

            result = fetch_url("https://example.com", timeout=3)

        self.assertEqual(
            result,
            FetchResult(
                status_code=200,
                reason="OK",
                body=b"<html>hello</html>",
            ),
        )
        self.assertEqual(urlopen.call_args.kwargs["timeout"], 3)
        self.assertEqual(urlopen.call_args.args[0].full_url, "https://example.com")

    def test_retries_failed_fetch_before_succeeding(self):
        with patch("public_directory_scraper.fetcher.urlopen") as urlopen:
            urlopen.side_effect = [OSError("temporary failure"), FakeResponse()]

            result = fetch_url("https://example.com", retries=1)

        self.assertEqual(result.body, b"<html>hello</html>")
        self.assertEqual(urlopen.call_count, 2)

    def test_rejects_negative_retries(self):
        with self.assertRaisesRegex(ValueError, "retries must be at least 0"):
            fetch_url("https://example.com", retries=-1)

    def test_rejects_unsupported_url_scheme(self):
        with self.assertRaisesRegex(ValueError, "URL scheme must be one of"):
            fetch_url("ftp://example.com/file")

    def test_allows_callers_to_restrict_url_schemes(self):
        with self.assertRaisesRegex(ValueError, "URL scheme must be one of: https"):
            fetch_url("file:///tmp/page.html", allowed_schemes={"https"})


if __name__ == "__main__":
    unittest.main()
