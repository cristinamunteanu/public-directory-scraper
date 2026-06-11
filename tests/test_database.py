import unittest

from public_directory_scraper.database import connect


class ConnectTest(unittest.TestCase):
    def test_connects_with_database_url(self):
        calls = []

        def fake_connector(database_url):
            calls.append(database_url)
            return "connection"

        connection = connect(
            "postgresql://localhost/public_directory_scraper",
            connector=fake_connector,
        )

        self.assertEqual(connection, "connection")
        self.assertEqual(calls, ["postgresql://localhost/public_directory_scraper"])

    def test_requires_database_url(self):
        with self.assertRaisesRegex(ValueError, "database_url is required"):
            connect("", connector=lambda database_url: database_url)


if __name__ == "__main__":
    unittest.main()
