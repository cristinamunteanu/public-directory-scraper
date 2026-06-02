# Public Directory Scraper

Minimal Python project structure for developing a public directory scraper in small, testable steps.

## Project Layout

```text
.
├── src/public_directory_scraper/
│   ├── __init__.py
│   ├── __main__.py
│   └── parser.py
├── tests/
│   ├── fixtures/
│   │   ├── listings.html
│   │   └── simple_listing.html
│   ├── test_cli_entrypoint.py
│   ├── test_parser.py
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

Run the package entrypoint:

```bash
PYTHONPATH=src .venv/bin/python -m public_directory_scraper
```

Parse saved HTML listings:

```bash
PYTHONPATH=src .venv/bin/python -m public_directory_scraper parse tests/fixtures/listings.html
```

Next recommended development step: save parsed results to CSV before adding network fetching.
