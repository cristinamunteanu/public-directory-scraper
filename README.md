# Public Directory Scraper

Minimal Python project structure for developing a public directory scraper in small, testable steps.

## Target

This project will scrape [Books to Scrape](https://books.toscrape.com/), a public sandbox website built for scraping practice.

Planned v1 fields:

- `title`
- `price`
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
│   ├── exporter.py
│   ├── fetcher.py
│   ├── parser.py
│   └── scraper.py
├── tests/
│   ├── fixtures/
│   │   ├── listings.html
│   │   └── simple_listing.html
│   ├── test_cli_entrypoint.py
│   ├── test_exporter.py
│   ├── test_fetcher.py
│   ├── test_parser.py
│   ├── test_scraper.py
│   └── test_import.py
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

Save parsed listings to CSV:

```bash
PYTHONPATH=src .venv/bin/python -m public_directory_scraper parse tests/fixtures/listings.html --output listings.csv
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

Current parser note: the parser still uses fixture-style `data-field` HTML markers. The next implementation step is to add a saved Books to Scrape fixture and adapt the parser to that page structure.
