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


if __name__ == "__main__":
    unittest.main()
