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

## 2026-06-03

Configured Ruff linting as a small development tool.

Why this structure:
- Ruff is listed as an optional `dev` dependency.
- Configuration lives in `pyproject.toml` with a narrow rule set: pycodestyle errors, Pyflakes, and import sorting.
- Formatting is not enabled yet, so linting stays separate from code rewriting.

How to test:

```bash
.venv/bin/python -m unittest discover -s tests
.venv/bin/ruff check src tests
```

Known limitations:
- No automatic formatter is configured.
- No CI or pre-commit hook runs linting automatically.

## 2026-06-03

Built the fifth vertical slice: friendly parse input errors.

Why this structure:
- Error handling stays close to the CLI file-reading and parsing path.
- Parser behavior remains unchanged; the CLI translates common failures into user-facing messages.
- Tests verify exit code, stdout, and stderr so the command-line contract is explicit.

How to test:

```bash
.venv/bin/python -m unittest discover -s tests
.venv/bin/ruff check src tests
.venv/bin/python -m public_directory_scraper parse missing.html
```

Known limitations:
- CSV output write errors are still not handled with friendly messages.
- No live fetching or pagination exists yet.

## 2026-06-03

Built the sixth vertical slice: fetch one URL.

Why this structure:
- `fetcher.py` contains network fetching logic outside the CLI.
- The CLI prints only status and byte count, so the first network behavior stays inspectable.
- Tests mock the fetcher core and use a local `file://` URL for CLI coverage, avoiding live internet dependency.

How to test:

```bash
.venv/bin/python -m unittest discover -s tests
.venv/bin/ruff check src tests
.venv/bin/python -m public_directory_scraper fetch https://example.com
```

Known limitations:
- Fetching is not connected to parsing yet.
- There are no retries, custom timeout option, saved response files, or pagination.
