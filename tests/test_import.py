import unittest

import public_directory_scraper


class PackageImportTest(unittest.TestCase):
    def test_package_imports(self):
        self.assertEqual(public_directory_scraper.__version__, "0.1.0")


if __name__ == "__main__":
    unittest.main()
