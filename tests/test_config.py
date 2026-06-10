import unittest

from public_directory_scraper.config import EtlConfig, load_config


class LoadConfigTest(unittest.TestCase):
    def test_loads_required_database_url_with_defaults(self):
        config = load_config(
            {
                "DATABASE_URL": (
                    "postgresql://postgres:postgres@localhost:5432/"
                    "public_directory_scraper"
                )
            }
        )

        self.assertEqual(
            config,
            EtlConfig(
                database_url=(
                    "postgresql://postgres:postgres@localhost:5432/"
                    "public_directory_scraper"
                ),
            ),
        )

    def test_loads_optional_defaults(self):
        config = load_config(
            {
                "DATABASE_URL": "postgresql://localhost/public_directory_scraper",
                "DEFAULT_PAGES": "2",
                "DEFAULT_TIMEOUT": "5.5",
                "DEFAULT_RETRIES": "1",
                "DEFAULT_DELAY": "0.5",
            }
        )

        self.assertEqual(config.default_pages, 2)
        self.assertEqual(config.default_timeout, 5.5)
        self.assertEqual(config.default_retries, 1)
        self.assertEqual(config.default_delay, 0.5)

    def test_requires_database_url(self):
        with self.assertRaisesRegex(ValueError, "DATABASE_URL is required"):
            load_config({})

    def test_rejects_invalid_default_pages(self):
        with self.assertRaisesRegex(ValueError, "DEFAULT_PAGES"):
            load_config(
                {
                    "DATABASE_URL": "postgresql://localhost/public_directory_scraper",
                    "DEFAULT_PAGES": "0",
                }
            )

    def test_rejects_invalid_default_delay(self):
        with self.assertRaisesRegex(ValueError, "DEFAULT_DELAY"):
            load_config(
                {
                    "DATABASE_URL": "postgresql://localhost/public_directory_scraper",
                    "DEFAULT_DELAY": "-1",
                }
            )


if __name__ == "__main__":
    unittest.main()
