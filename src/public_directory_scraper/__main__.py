import json
import sys
from pathlib import Path

from . import __version__
from .exporter import write_records_csv
from .fetcher import fetch_url
from .parser import parse_listings
from .scraper import scrape_url


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)

    if args:
        command = args[0]
        if command == "fetch" and len(args) == 2:
            url = args[1]

            try:
                result = fetch_url(url)
            except (OSError, ValueError) as error:
                print(f"Error: could not fetch {url}: {error}", file=sys.stderr)
                return 1

            print(f"{result.status_code} {result.reason}")
            print(f"bytes: {len(result.body)}")
            return 0

        if command == "scrape" and len(args) == 2:
            url = args[1]

            try:
                records = scrape_url(url)
            except (OSError, ValueError) as error:
                print(f"Error: could not scrape {url}: {error}", file=sys.stderr)
                return 1

            print(json.dumps(records))
            return 0

        if command == "parse" and len(args) in {2, 4}:
            input_path = args[1]

            try:
                html = Path(input_path).read_text(encoding="utf-8")
                records = parse_listings(html)
            except FileNotFoundError:
                print(f"Error: file not found: {input_path}", file=sys.stderr)
                return 1
            except IsADirectoryError:
                print(
                    f"Error: expected a file, got directory: {input_path}",
                    file=sys.stderr,
                )
                return 1
            except ValueError as error:
                print(f"Error: {error}", file=sys.stderr)
                return 1

            if len(args) == 4 and args[2] == "--output":
                count = write_records_csv(records, args[3])
                print(f"Wrote {count} records to {args[3]}")
                return 0

            if len(args) == 2:
                print(json.dumps(records))
                return 0

        usage = (
            "Usage: python -m public_directory_scraper "
            "[fetch URL | scrape URL | parse HTML_FILE [--output OUTPUT.csv]]"
        )
        print(usage, file=sys.stderr)
        return 2

    print(f"public-directory-scraper {__version__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
