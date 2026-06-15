# Public Directory Scraper

A small Python scraper that collects book listing data from [Books to Scrape](https://books.toscrape.com/), cleans the records, and saves them to CSV or Excel.

Books to Scrape is a public sandbox website built for scraping practice.

## What It Scrapes

The scraper extracts book cards from listing pages.

Fields:

- `title`
- `price_gbp`
- `availability`
- `rating`
- `book_url`
- `image_url`

The scraper can follow pagination with `--pages N`, retry temporary fetch failures with `--retries N`, pause between paginated requests with `--delay SECONDS`, remove duplicate books by `book_url`, and write output files with `.csv` or `.xlsx` extensions.

## How To Run

Create a virtual environment and install the project:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
```

Run against the live site:

```bash
.venv/bin/python -m public_directory_scraper scrape https://books.toscrape.com/ --pages 2 --timeout 10 --retries 1 --delay 1 --output books.csv
```

Run the ETL pipeline after setting `DATABASE_URL`:

```bash
.venv/bin/python -m public_directory_scraper etl https://books.toscrape.com/ --run-id books-001 --pages 2 --timeout 10 --retries 1 --delay 1
```

Save Excel output instead:

```bash
.venv/bin/python -m public_directory_scraper scrape https://books.toscrape.com/ --pages 2 --timeout 10 --retries 1 --delay 1 --output books.xlsx
```

Run against the local fixture without internet access:

```bash
.venv/bin/python -m public_directory_scraper scrape file:///absolute/path/to/books_page.html --pages 2 --output books.csv
```

Fetch a single page with retry and timeout options:

```bash
.venv/bin/python -m public_directory_scraper fetch https://books.toscrape.com/ --timeout 10 --retries 1
```

## Sample Output

The checked-in sample output is available at [sample_outputs/books_sample.csv](sample_outputs/books_sample.csv).

Preview:

| title | price_gbp | availability | rating |
| --- | ---: | --- | ---: |
| A Light in the Attic | 51.77 | In stock | 3 |
| Tipping the Velvet | 53.74 | In stock | 1 |
| The Republic | 33.78 | In stock | 4 |

The full CSV also includes `book_url` and `image_url`.

Screenshot:

![Books scraper CSV output preview](docs/screenshots/books-output.svg)

## Development

Run tests:

```bash
.venv/bin/python -m unittest discover -s tests
```

Run linting:

```bash
.venv/bin/ruff check src tests
```

Useful local commands:

```bash
.venv/bin/python -m public_directory_scraper
.venv/bin/python -m public_directory_scraper parse tests/fixtures/books_page.html
.venv/bin/python -m public_directory_scraper fetch https://books.toscrape.com/
.venv/bin/python -m public_directory_scraper etl https://books.toscrape.com/ --run-id manual-test
```

## ETL Configuration

The project is being extended toward a small Postgres ETL pipeline. Current ETL support includes configuration loading, a small Postgres connection wrapper, schema creation helpers, raw extraction, raw/cleaned table loaders, and a core ETL pipeline function.

Copy the example environment file when you are ready to configure local database settings:

```bash
cp .env.example .env
```

The `etl` command loads `.env` automatically. Existing shell environment variables
are not overwritten by `.env` values. The parser supports `KEY=value`,
`export KEY=value`, blank lines, comments, and simple inline comments.

Current ETL-related environment variables:

- `DATABASE_URL`
- `DEFAULT_PAGES`
- `DEFAULT_TIMEOUT`
- `DEFAULT_RETRIES`
- `DEFAULT_DELAY`

The ETL command logs start, success, and failure events through Python's standard
`logging` module. It does not write log files by default.

## Local Postgres Check

Use this manual check when you have Postgres installed locally.

Create the database:

```bash
createdb public_directory_scraper
```

Prepare local settings:

```bash
cp .env.example .env
```

Edit `.env` if your local Postgres username, password, host, or port is different.

Run one small ETL load:

```bash
.venv/bin/python -m public_directory_scraper etl https://books.toscrape.com/ --run-id local-check --pages 1 --timeout 10 --retries 1 --delay 0
```

Expected command output:

```text
Raw records loaded: 20
Cleaned records loaded: 20
```

Inspect the loaded tables:

```bash
psql public_directory_scraper -c "SELECT COUNT(*) FROM raw_books;"
psql public_directory_scraper -c "SELECT COUNT(*) FROM cleaned_books;"
psql public_directory_scraper -c "SELECT title, price_gbp, rating FROM cleaned_books LIMIT 5;"
```

Remove the local database when you are done:

```bash
dropdb public_directory_scraper
```

Run the optional Postgres integration test against that database:

```bash
INTEGRATION_DATABASE_URL=postgresql://postgres:postgres@localhost:5432/public_directory_scraper .venv/bin/python -m unittest tests.test_postgres_integration
```

The normal test command skips this integration test unless `INTEGRATION_DATABASE_URL`
is set.

## Project Layout

```text
.
├── src/public_directory_scraper/
│   ├── __init__.py
│   ├── __main__.py
│   ├── config.py
│   ├── cleaner.py
│   ├── database.py
│   ├── exporter.py
│   ├── fetcher.py
│   ├── loader.py
│   ├── parser.py
│   ├── pipeline.py
│   ├── schema.py
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
│   ├── test_config.py
│   ├── test_database.py
│   ├── test_cli_entrypoint.py
│   ├── test_exporter.py
│   ├── test_fetcher.py
│   ├── test_loader.py
│   ├── test_parser.py
│   ├── test_pipeline.py
│   ├── test_schema.py
│   ├── test_scraper.py
│   └── test_import.py
├── sample_outputs/
│   └── books_sample.csv
├── docs/
│   └── screenshots/
│       └── books-output.svg
├── .env.example
├── pyproject.toml
├── README.md
└── DEV_LOG.md
```

## How It Works

- `fetcher.py` downloads one page.
- `parser.py` extracts raw listing records from HTML.
- `cleaner.py` normalizes prices, ratings, text, URLs, and duplicates.
- `scraper.py` connects fetching, parsing, cleaning, raw extraction, and pagination.
- `exporter.py` writes records to CSV or Excel.
- `config.py` reads future ETL settings from environment variables.
- `database.py` opens future Postgres connections.
- `loader.py` inserts raw and cleaned records into Postgres.
- `pipeline.py` extracts raw records, loads raw rows, cleans records, and loads cleaned rows.
- `schema.py` creates future raw and cleaned Postgres tables.
- `__main__.py` exposes the command-line interface.

## Limitations

- The parser is tailored to Books to Scrape listing pages.
- Pagination is limited by the `--pages` value.
- Retries are immediate; there is no exponential backoff.
- Crawl delay is fixed between paginated requests.
- The local CLI allows `file://` URLs for fixture-based development; production reuse should restrict input URLs to trusted `http` or `https` targets.
- The ETL command requires a reachable Postgres database through `DATABASE_URL`.
- `.env` loading intentionally supports only simple one-line values.
- ETL logging uses the standard logging module, but no file or JSON logging is configured.
- There is no live-site change detection yet.
- The screenshot is a static preview of the sample output.
- The sample CSV is static and should be refreshed if output fields change.
