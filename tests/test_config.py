import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from public_directory_scraper.config import EtlConfig, load_config, load_env_file


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

    def test_loads_env_file_without_overwriting_existing_values(self):
        with TemporaryDirectory() as temp_dir:
            env_path = Path(temp_dir) / ".env"
            env_path.write_text(
                "\n".join(
                    [
                        "# local settings",
                        "DATABASE_URL=postgresql://from-file/database",
                        "DEFAULT_PAGES=2",
                        "DEFAULT_TIMEOUT='5.5'",
                    ]
                ),
                encoding="utf-8",
            )
            values = {"DATABASE_URL": "postgresql://from-shell/database"}

            loaded_count = load_env_file(env_path, environ=values)

        self.assertEqual(loaded_count, 2)
        self.assertEqual(values["DATABASE_URL"], "postgresql://from-shell/database")
        self.assertEqual(values["DEFAULT_PAGES"], "2")
        self.assertEqual(values["DEFAULT_TIMEOUT"], "5.5")

    def test_ignores_missing_env_file(self):
        with TemporaryDirectory() as temp_dir:
            loaded_count = load_env_file(Path(temp_dir) / ".env", environ={})

        self.assertEqual(loaded_count, 0)

    def test_rejects_invalid_env_file_line(self):
        with TemporaryDirectory() as temp_dir:
            env_path = Path(temp_dir) / ".env"
            env_path.write_text("DATABASE_URL\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "invalid .env line 1"):
                load_env_file(env_path, environ={})


if __name__ == "__main__":
    unittest.main()
