# Public Directory Scraper

Minimal Python project structure for developing a public directory scraper in small, testable steps.

## Project Layout

```text
.
├── src/public_directory_scraper/
│   └── __init__.py
├── tests/
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

Next recommended development step: define the smallest core scraping function before adding CLI or UI behavior.
