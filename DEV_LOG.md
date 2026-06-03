# Development Log

## 2026-06-01

Built a minimal Python project skeleton for small-step scraper development.

Why this structure:
- `src/` keeps package code separate from tests and project files.
- `tests/` gives the project an immediate validation loop.
- No scraper logic or third-party runtime dependencies were added yet.

How to test:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

Known limitations:
- No scraping behavior exists yet.
- The first real feature should start in core logic before any CLI or UI layer.

## 2026-06-02

Built the first vertical slice: a runnable package entrypoint.

Why this structure:
- `__main__.py` keeps the visible command behavior small and easy to test.
- The subprocess test verifies the same module execution path a user runs manually.

How to test:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
PYTHONPATH=src python3 -m public_directory_scraper
```

Known limitations:
- The command only prints the package name and version.
- No scraping, parsing, fetching, or file output exists yet.

## 2026-06-02

Built the second vertical slice: parse one saved HTML listing.

Why this structure:
- `parser.py` contains core parsing logic outside the CLI entrypoint.
- The CLI reads a local HTML file and prints JSON, so the behavior is visible without network access.
- The parser uses standard-library `HTMLParser` to avoid adding dependencies before a real target site requires them.

How to test:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
PYTHONPATH=src python3 -m public_directory_scraper parse tests/fixtures/simple_listing.html
```

Known limitations:
- It only parses one listing.
- It expects fixture-style `data-field` markers for `name` and `url`.
- No live fetching, pagination, or CSV export exists yet.

## 2026-06-02

Built the third vertical slice: parse multiple saved HTML listings.

Why this structure:
- `parse_listings()` is the core multi-record function.
- `parse_listing()` remains as a small compatibility helper for one-record tests and examples.
- The CLI now prints a JSON array, matching the shape needed for CSV export later.

How to test:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
PYTHONPATH=src python3 -m public_directory_scraper parse tests/fixtures/listings.html
```

Known limitations:
- It still expects fixture-style `data-field` markers.
- It does not fetch live pages, follow pagination, or write files.

## 2026-06-02

Built the fourth vertical slice: save parsed listings to CSV.

Why this structure:
- `exporter.py` contains CSV writing logic outside the CLI.
- The CLI keeps JSON output as the default and only writes CSV when `--output` is provided.
- CSV uses the standard library and fixed `name,url` fields.

How to test:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
PYTHONPATH=src python3 -m public_directory_scraper parse tests/fixtures/listings.html --output listings.csv
```

Known limitations:
- It does not create missing output directories.
- It still expects fixture-style HTML markers.
- No live fetching, pagination, or friendly missing-file errors exist yet.
