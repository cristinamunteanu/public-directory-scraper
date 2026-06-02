import json
import os
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIXTURES_DIR = PROJECT_ROOT / "tests" / "fixtures"


class CliEntrypointTest(unittest.TestCase):
    def test_package_runs_as_module(self):
        env = os.environ.copy()
        env["PYTHONPATH"] = str(PROJECT_ROOT / "src")

        result = subprocess.run(
            [sys.executable, "-m", "public_directory_scraper"],
            check=True,
            capture_output=True,
            env=env,
            text=True,
        )

        self.assertEqual(result.stdout.strip(), "public-directory-scraper 0.1.0")
        self.assertEqual(result.stderr, "")

    def test_parse_command_prints_listing_json(self):
        env = os.environ.copy()
        env["PYTHONPATH"] = str(PROJECT_ROOT / "src")

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "public_directory_scraper",
                "parse",
                str(FIXTURES_DIR / "listings.html"),
            ],
            check=True,
            capture_output=True,
            env=env,
            text=True,
        )

        self.assertEqual(
            json.loads(result.stdout),
            [
                {
                    "name": "Example Business",
                    "url": "https://example.com",
                },
                {
                    "name": "Second Business",
                    "url": "https://second.example",
                },
            ],
        )
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
