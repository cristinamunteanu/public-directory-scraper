# Public Directory Scraper

Minimal Python project structure for developing a public directory scraper in small, testable steps.

## Target

This project will scrape [Books to Scrape](https://books.toscrape.com/), a public sandbox website built for scraping practice.

Planned v1 fields:

- `title`
- `price_gbp`
- `availability`
- `rating`
- `book_url`
- `image_url`

## Project Layout

```text
.
├── src/public_directory_scraper/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cleaner.py
│   ├── exporter.py
│   ├── fetcher.py
│   ├── parser.py
│   └── scraper.py
├── tests/
│   ├── fixtures/
│   │   ├── books_page.html
│   │   ├── catalogue/
│   │   │   └── page-2.html
│   │   ├── listings.html
│   │   └── simple_listing.html
│   ├── test_books_fixture.py
│   ├── test_cleaner.py
│   ├── test_cli_entrypoint.py
│   ├── test_exporter.py
│   ├── test_fetcher.py
│   ├── test_parser.py
│   ├── test_scraper.py
│   └── test_import.py
├── sample_outputs/
│   └── books_sample.csv
├── pyproject.toml
├── README.md
└── DEV_LOG.md
```

## Development

Create a virtual environment and install the package in editable mode:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e .
```

Run the current test suite:

```bash
.venv/bin/python -m unittest discover -s tests
```

Run linting:

```bash
.venv/bin/ruff check src tests
```

Run the package entrypoint:

```bash
PYTHONPATH=src .venv/bin/python -m public_directory_scraper
```

Parse saved HTML listings:

```bash
PYTHONPATH=src .venv/bin/python -m public_directory_scraper parse tests/fixtures/listings.html
```

Parse the Books to Scrape fixture:

```bash
.venv/bin/python -m public_directory_scraper parse tests/fixtures/books_page.html
```

Save parsed listings to CSV:

```bash
PYTHONPATH=src .venv/bin/python -m public_directory_scraper parse tests/fixtures/listings.html --output listings.csv
```

Save parsed Books records to CSV:

```bash
.venv/bin/python -m public_directory_scraper parse tests/fixtures/books_page.html --output books.csv
```

If the input file is missing or does not contain a valid listing, the command prints an `Error:` message to stderr and exits with a non-zero status.

Fetch one URL:

```bash
.venv/bin/python -m public_directory_scraper fetch https://example.com
```

Fetch and parse one URL:

```bash
.venv/bin/python -m public_directory_scraper scrape file:///absolute/path/to/listings.html
```

Fetch, parse, clean, and save Books records to CSV:

```bash
.venv/bin/python -m public_directory_scraper scrape file:///absolute/path/to/books_page.html --output books.csv
```

Fetch and parse a limited number of paginated Books pages:

```bash
.venv/bin/python -m public_directory_scraper scrape file:///absolute/path/to/books_page.html --pages 2 --output books.csv
```

Save scraped Books records to Excel:

```bash
.venv/bin/python -m public_directory_scraper scrape file:///absolute/path/to/books_page.html --output books.xlsx
```

## Sample Output

The checked-in sample output is available at `sample_outputs/books_sample.csv`.

Generate a comparable CSV from the local two-page fixture:

```bash
.venv/bin/python -m public_directory_scraper scrape file:///absolute/path/to/books_page.html --pages 2 --output books.csv
```

Preview:

| title | price_gbp | availability | rating |
| --- | ---: | --- | ---: |
| A Light in the Attic | 51.77 | In stock | 3 |
| Tipping the Velvet | 53.74 | In stock | 1 |
| The Republic | 33.78 | In stock | 4 |

The full CSV also includes `book_url` and `image_url`.

## Limitations

- The parser is tailored to Books to Scrape listing pages.
- Pagination is limited by the `--pages` value.
- There is no crawl delay, retry policy, or live-site change detection yet.
- Output screenshots are not included yet.

Books to Scrape fixture note: `tests/fixtures/books_page.html` contains a compact representative page with two `product_pod` book cards and pagination markup. The parser extracts the planned v1 book fields from this fixture.

Books cleaning note: scraped Books records normalize `price` into `price_gbp`, convert rating words to numbers, trim text fields, and turn relative book/image paths into absolute URLs.

Output note: CSV and Excel headers are inferred from record fields, so both legacy `name,url` records and Books records can be written.
