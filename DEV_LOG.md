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

## 2026-06-03

Built the seventh vertical slice: fetch and parse one page.

Why this structure:
- `scraper.py` connects the existing fetcher and parser without mixing logic into the CLI.
- The CLI `scrape URL` command prints the same JSON array shape as `parse`.
- Tests use mocked fetching for core logic and a local `file://` fixture for CLI behavior.

How to test:

```bash
.venv/bin/python -m unittest discover -s tests
.venv/bin/ruff check src tests
.venv/bin/python -m public_directory_scraper scrape file:///absolute/path/to/listings.html
```

Known limitations:
- It assumes UTF-8 response content.
- It still expects fixture-style `data-field` HTML markers.
- No pagination, retries, CSV output for scraped URLs, or target-site-specific parser exists yet.

## 2026-06-04

Chose the real target site for the scraper: `https://books.toscrape.com/`.

Why this target:
- It is a public sandbox website intended for scraping practice.
- The listing page has repeated book cards, prices, stock text, ratings, detail links, image links, and pagination.
- It is stable enough for a beginner portfolio scraper without using a real commercial site.

Planned v1 fields:
- `title`
- `price`
- `availability`
- `rating`
- `book_url`
- `image_url`

Important tradeoffs:
- This slice documents the target only; it does not change parser behavior yet.
- The current parser still expects fixture-style `data-field` markers.

How to test:

```bash
.venv/bin/python -m unittest discover -s tests
.venv/bin/ruff check src tests
```

Known limitations:
- No Books to Scrape fixture has been added yet.
- The parser has not been adapted to the real Books to Scrape HTML.

Next recommended step:
- Save a small Books to Scrape HTML fixture and write parser tests against it.

## 2026-06-04

Added a compact Books to Scrape HTML fixture.

Why this structure:
- The fixture keeps only representative product card and pagination markup instead of the full live page.
- It includes two `product_pod` records with title, detail URL, image URL, rating class, price, and availability text.
- A small fixture-shape test verifies the expected selectors exist before parser work begins.

Important tradeoffs:
- This slice does not adapt `parser.py` yet.
- The fixture is intentionally small so the next parser change is easy to inspect.

How to test:

```bash
.venv/bin/python -m unittest discover -s tests
.venv/bin/ruff check src tests
```

Known limitations:
- The current parser still ignores Books to Scrape markup.
- The fixture covers only the first-page card shape and a `next` pagination link.

Next recommended step:
- Update `parser.py` to extract Books to Scrape fields from `books_page.html`.

## 2026-06-04

Updated the parser to extract Books to Scrape fields from the saved fixture.

Why this structure:
- The legacy `data-field` parser behavior remains in place for earlier tests and examples.
- Books parsing is selected when the HTML contains `product_pod` cards.
- The parser extracts the planned v1 fields: title, price, availability, rating, book URL, and image URL.

Important tradeoffs:
- URLs are still extracted as relative URLs from the page.
- Cleaning, deduplication, CSV field updates, Excel export, and pagination are not part of this slice.

How to test:

```bash
.venv/bin/python -m unittest discover -s tests
.venv/bin/ruff check src tests
.venv/bin/python -m public_directory_scraper parse tests/fixtures/books_page.html
```

Known limitations:
- The parser covers the saved first-page fixture shape only.
- It does not normalize prices, convert ratings to numbers, or follow pagination.

Next recommended step:
- Add a cleaning layer for Books records.

## 2026-06-04

Added a cleaning layer for Books to Scrape records.

Why this structure:
- `cleaner.py` keeps normalization separate from parser extraction.
- `parse` still returns raw extracted fields for inspection.
- `scrape_url()` cleans Books records after fetching and parsing, which matches the end-to-end scraper path.

What it cleans:
- trims text fields
- converts `price` strings into `price_gbp` floats
- converts rating words into numbers
- converts relative book and image paths into absolute URLs
- handles missing values with empty strings

How to test:

```bash
.venv/bin/python -m unittest discover -s tests
.venv/bin/ruff check src tests
```

Known limitations:
- Cleaning is only integrated into the `scrape_url()` path, not `parse`.
- No duplicate removal, CSV field update, Excel export, or pagination exists yet.

Next recommended step:
- Update CSV export to support Books records.

## 2026-06-05

Updated CSV export to support Books records.

Why this structure:
- CSV headers are inferred from record keys in first-seen order.
- Legacy `name,url` records still write the same CSV shape.
- Books parser records can now be written to CSV without changing parser output.

Important tradeoffs:
- This supports `parse books_page.html --output books.csv`.
- It does not add `scrape URL --output` yet.
- Books CSV from `parse` is raw parser output, not cleaned `scrape_url()` output.

How to test:

```bash
.venv/bin/python -m unittest discover -s tests
.venv/bin/ruff check src tests
.venv/bin/python -m public_directory_scraper parse tests/fixtures/books_page.html --output /tmp/books.csv
```

Known limitations:
- Scraped Books records cannot be written directly with `scrape --output` yet.
- Excel export and pagination are still not implemented.

Next recommended step:
- Add `scrape URL --output results.csv`.

## 2026-06-05

Added CSV output for scraped pages.

Why this structure:
- The `scrape` command now mirrors the existing `parse --output` option.
- It reuses `scrape_url()` for fetching, parsing, and Books cleaning.
- It reuses `write_records_csv()` for output, so no new export path was added.

How to test:

```bash
.venv/bin/python -m unittest discover -s tests
.venv/bin/ruff check src tests
.venv/bin/python -m public_directory_scraper scrape file:///absolute/path/to/books_page.html --output /tmp/books.csv
```

Known limitations:
- Only CSV output is supported.
- Excel export and pagination are still not implemented.

Next recommended step:
- Add Excel export or pagination, depending on which deliverable requirement should come first.

## 2026-06-05

Added Excel export support.

Why this structure:
- `write_records()` dispatches output based on the file extension.
- `.csv` output keeps using the standard-library CSV writer.
- `.xlsx` output uses `openpyxl` and writes one sheet named `records`.
- Existing `parse --output` and `scrape --output` commands can now write CSV or Excel files.

Important tradeoffs:
- Excel output is intentionally plain: no styling, filters, widths, or multiple sheets.
- Unsupported output extensions fail with a clear `ValueError`.

How to test:

```bash
.venv/bin/python -m unittest discover -s tests
.venv/bin/ruff check src tests
.venv/bin/python -m public_directory_scraper scrape file:///absolute/path/to/books_page.html --output /tmp/books.xlsx
```

Known limitations:
- Pagination is still not implemented.
- README does not yet include screenshots or final sample output.

Next recommended step:
- Add pagination or final README deliverable polish.

## 2026-06-05

Added limited pagination for scraped Books pages.

Why this structure:
- `parse_next_page_url()` extracts the Books pagination `next` link.
- `scrape_pages()` follows next links up to a caller-provided page limit.
- The CLI supports `scrape URL --pages N` and can combine it with `--output`.
- Tests use local fixtures, including `tests/fixtures/catalogue/page-2.html`, so pagination checks do not depend on live network access.

How to test:

```bash
.venv/bin/python -m unittest discover -s tests
.venv/bin/ruff check src tests
.venv/bin/python -m public_directory_scraper scrape file:///absolute/path/to/books_page.html --pages 2 --output /tmp/books.csv
```

Known limitations:
- Pagination is capped by the user-provided `--pages` value.
- There is no crawl delay, retry policy, or duplicate removal yet.
- The final README still needs sample output and screenshots.

Next recommended step:
- Add duplicate removal or final README deliverable polish.

## 2026-06-07

Added duplicate removal for scraped Books records.

Why this structure:
- `deduplicate_records()` keeps duplicate handling in the cleaning layer.
- `scrape_pages()` removes duplicates after collecting records from all requested pages.
- The first record wins, which keeps output deterministic and easy to inspect.

Important tradeoffs:
- Duplicates are identified by non-empty `book_url` values only.
- Records with missing `book_url` values are kept instead of being silently dropped.

How to test:

```bash
.venv/bin/python -m unittest discover -s tests
.venv/bin/ruff check src tests
```

Known limitations:
- There is no crawl delay or retry policy yet.
- The final README still needs sample output and screenshots.

Next recommended step:
- Add final README sample output and output-file screenshots.

## 2026-06-07

Added a checked-in sample CSV output and README sample-output section.

Why this structure:
- `sample_outputs/books_sample.csv` gives the repo a visible output artifact.
- The README shows a compact preview table instead of requiring readers to open the CSV first.
- Limitations are now grouped in a dedicated README section.

Important tradeoffs:
- The sample uses target-site-style URLs so it stays portable across machines.
- Output screenshots are left for a separate slice.

How to test:

```bash
.venv/bin/python -m unittest discover -s tests
.venv/bin/ruff check src tests
.venv/bin/python -m public_directory_scraper scrape file:///absolute/path/to/books_page.html --pages 2 --output /tmp/books.csv
```

Known limitations:
- The sample CSV is static and should be refreshed if output fields change.
- README screenshots are still missing.

Next recommended step:
- Add a small screenshot asset showing the generated output file.

## 2026-06-07

Added a README screenshot asset for the sample output.

Why this structure:
- `docs/screenshots/books-output.svg` is small, readable, and renders directly in GitHub.
- The screenshot preview is documentation-only, so it does not affect scraper behavior.
- The README now links the sample CSV and shows the visual output shape.

Important tradeoffs:
- The screenshot is a static preview, not generated automatically from the CSV.
- No code or dependency changes were made in this slice.

How to test:

```bash
.venv/bin/python -m unittest discover -s tests
.venv/bin/ruff check src tests
```

Known limitations:
- The screenshot should be refreshed if output fields change.
- A live scrape command still depends on network access.

Next recommended step:
- Do a final README pass for portfolio readiness.

## 2026-06-07

Polished the README for portfolio readiness.

Why this structure:
- The README now starts with the finished scraper behavior instead of the project skeleton.
- Run commands focus on the real target site, with a local fixture command for offline checks.
- Project structure and module responsibilities are still documented for inspection.

Important tradeoffs:
- No implementation behavior changed in this slice.
- Live-site commands are documented but not required for the test suite.

How to test:

```bash
.venv/bin/python -m unittest discover -s tests
.venv/bin/ruff check src tests
```

Known limitations:
- The live scrape command depends on network access.
- The screenshot and sample CSV are static documentation assets.

Next recommended step:
- Run one live scrape check when network access is available.

## 2026-06-07

Ignored root-level generated output files.

Why this structure:
- Root-level `.csv` and `.xlsx` files are common manual scraper outputs.
- The ignore rules are root-only, so checked-in samples under `sample_outputs/` remain trackable.

Important tradeoffs:
- Existing generated files are not deleted.
- Output files in subdirectories can still be committed deliberately.

How to test:

```bash
.venv/bin/python -m unittest discover -s tests
.venv/bin/ruff check src tests
git status --short
```

Known limitations:
- This does not clean up any local generated files.

Next recommended step:
- Run one live scrape check when network access is available.

## 2026-06-08

Ran a live scrape check against Books to Scrape.

Why this structure:
- The check uses the same command documented in the README.
- Output was written to `/tmp` so no generated live output file is added to the repo.
- The command fetched two pages and wrote 40 records.

Command:

```bash
.venv/bin/python -m public_directory_scraper scrape https://books.toscrape.com/ --pages 2 --output /tmp/public-directory-scraper-live-check.csv
```

Important tradeoffs:
- The live check depends on network access and the target site being available.
- The test suite still uses local fixtures so normal validation remains deterministic.

How to test:

```bash
.venv/bin/python -m unittest discover -s tests
.venv/bin/ruff check src tests
```

Known limitations:
- There is no crawl delay, retry policy, or live-site change detection yet.

Next recommended step:
- Consider the v1 portfolio scraper complete unless adding optional resilience features.

## 2026-06-08

Added core fetch retry support.

Why this structure:
- `fetch_url()` now accepts `retries` while keeping the default at zero extra attempts.
- Retry behavior lives in the fetcher layer, where network errors happen.
- The CLI is unchanged so this slice stays small and easy to inspect.

Important tradeoffs:
- Retries happen immediately without backoff or delay.
- The retry option is available to code callers but is not exposed as a CLI flag yet.

How to test:

```bash
.venv/bin/python -m unittest discover -s tests
.venv/bin/ruff check src tests
```

Known limitations:
- There is no `--retries` CLI option yet.
- There is no crawl delay or backoff yet.

Next recommended step:
- Add a CLI timeout option.

## 2026-06-08

Added a CLI timeout option for fetch and scrape commands.

Why this structure:
- `fetch URL --timeout SECONDS` passes timeout directly to `fetch_url()`.
- `scrape URL --timeout SECONDS` passes timeout through `scrape_pages()` to each fetched page.
- Timeout parsing is shared by both commands and rejects non-positive values.

Important tradeoffs:
- This slice does not expose retry settings through the CLI.
- Timeout is documented in code and tests, but README command examples are unchanged.

How to test:

```bash
.venv/bin/python -m unittest discover -s tests
.venv/bin/ruff check src tests
.venv/bin/python -m public_directory_scraper fetch file:///absolute/path/to/books_page.html --timeout 2.5
```

Known limitations:
- There is no CLI retry option yet.
- There is no crawl delay or backoff yet.

Next recommended step:
- Add a crawl delay option.

## 2026-06-08

Added a crawl delay option for paginated scraping.

Why this structure:
- `scrape_pages()` accepts `delay` and sleeps only between page requests.
- `scrape --delay SECONDS` exposes that behavior for manual live scraping.
- Delay validation allows `0` as the no-delay default and rejects negative values.

Important tradeoffs:
- Delay is not backoff; it is a fixed pause between successful page transitions.
- The fetch command does not accept delay because it downloads only one URL.

How to test:

```bash
.venv/bin/python -m unittest discover -s tests
.venv/bin/ruff check src tests
.venv/bin/python -m public_directory_scraper scrape file:///absolute/path/to/books_page.html --pages 2 --delay 0
```

Known limitations:
- There is no CLI retry option yet.
- There is no exponential backoff.

Next recommended step:
- Improve Excel output formatting.

## 2026-06-08

Improved Excel output formatting.

Why this structure:
- Excel formatting stays inside `exporter.py`, next to workbook creation.
- The header row is frozen and bolded so exported files are easier to inspect.
- Column widths are derived from content with simple min/max bounds.

Important tradeoffs:
- Formatting is intentionally plain: no filters, colors, number formats, or styling themes.
- CSV output is unchanged.

How to test:

```bash
.venv/bin/python -m unittest discover -s tests
.venv/bin/ruff check src tests
.venv/bin/python -m public_directory_scraper scrape file:///absolute/path/to/books_page.html --output /tmp/books.xlsx
```

Known limitations:
- Excel formatting is basic and intended only for readability.

Next recommended step:
- Stop feature work for this small portfolio scraper unless a new requirement appears.

## 2026-06-08

Handled output write failures in the CLI.

Why this structure:
- `parse --output` and `scrape --output` now catch filesystem write errors.
- Unsupported extensions still return usage-style errors, while write failures return runtime errors.
- Tests cover missing output directories for both command paths.

Important tradeoffs:
- The exporter still leaves directory creation to the caller.
- Error text includes the original operating-system message for debugging.

How to test:

```bash
.venv/bin/python -m unittest discover -s tests
.venv/bin/ruff check src tests
```

Known limitations:
- Output directories are not created automatically.

Next recommended step:
- Decide whether output directories should be created automatically or remain explicit.

## 2026-06-08

Exposed retry support through scraper and CLI commands.

Why this structure:
- `scrape_pages()` now passes retries to each `fetch_url()` call.
- `fetch --retries N` and `scrape --retries N` make the existing retry support usable.
- Retry validation requires a zero or positive integer.

Important tradeoffs:
- Retries are immediate; there is still no exponential backoff.
- Retry behavior stays simple and does not change the default of zero retries.

How to test:

```bash
.venv/bin/python -m unittest discover -s tests
.venv/bin/ruff check src tests
.venv/bin/python -m public_directory_scraper fetch file:///absolute/path/to/books_page.html --retries 1
```

Known limitations:
- There is no retry delay or backoff.

Next recommended step:
- Update README limitations and command examples for timeout, delay, and retries.

## 2026-06-08

Updated README retry and delay documentation.

Why this structure:
- The README now lists timeout, retries, and delay in the main run examples.
- Limitations no longer claim crawl delay or retry support is missing.
- Remaining limitations describe the current behavior: fixed delay and immediate retries.

Important tradeoffs:
- This is documentation-only; no code behavior changed.

How to test:

```bash
.venv/bin/python -m unittest discover -s tests
.venv/bin/ruff check src tests
```

Known limitations:
- README examples still use small page counts for portfolio-friendly runs.

Next recommended step:
- Re-review the remaining findings and choose the next small fix.

## 2026-06-09

Removed raw substring parser dispatch.

Why this structure:
- `parse_listings()` now tries fixture-style records structurally before trying Books records.
- Books parsing depends on actual product card records, not a plain `"product_pod"` text match.
- A regression test covers HTML where `product_pod` appears only as text.

Important tradeoffs:
- Parser mode is still inferred from markup rather than passed explicitly.
- Invalid partial records still fail through the generic listing error when no complete parser output exists.

How to test:

```bash
.venv/bin/python -m unittest discover -s tests
.venv/bin/ruff check src tests
```

Known limitations:
- The parser is still tailored to fixture-style listings and Books to Scrape cards.

Next recommended step:
- Harden malformed price handling.
