import json
import sys
from pathlib import Path

from . import __version__
from .exporter import write_records
from .fetcher import fetch_url
from .parser import parse_listings
from .scraper import scrape_pages


def _parse_positive_float(value, option_name):
    """Parse a positive floating-point option value."""
    try:
        number = float(value)
    except ValueError as error:
        raise ValueError(f"{option_name} must be a positive number") from error

    if number <= 0:
        raise ValueError(f"{option_name} must be a positive number")

    return number


def _parse_fetch_options(options):
    """Parse fetch-only options and return timeout seconds."""
    timeout = 10
    index = 0

    while index < len(options):
        option = options[index]

        if option == "--timeout":
            if index + 1 >= len(options):
                raise ValueError("--timeout requires a value")

            timeout = _parse_positive_float(options[index + 1], "--timeout")
            index += 2
            continue

        raise ValueError(f"unknown fetch option: {option}")

    return timeout


def _parse_scrape_options(options):
    """Parse scrape-only options and return page limit plus output path."""
    max_pages = 1
    output_path = None
    timeout = 10
    index = 0

    while index < len(options):
        option = options[index]

        if option == "--pages":
            if index + 1 >= len(options):
                raise ValueError("--pages requires a value")

            try:
                max_pages = int(options[index + 1])
            except ValueError as error:
                raise ValueError("--pages must be a positive integer") from error

            if max_pages < 1:
                raise ValueError("--pages must be a positive integer")

            index += 2
            continue

        if option == "--timeout":
            if index + 1 >= len(options):
                raise ValueError("--timeout requires a value")

            timeout = _parse_positive_float(options[index + 1], "--timeout")
            index += 2
            continue

        if option == "--output":
            if index + 1 >= len(options):
                raise ValueError("--output requires a path")

            output_path = options[index + 1]
            index += 2
            continue

        raise ValueError(f"unknown scrape option: {option}")

    return max_pages, output_path, timeout


def main(argv=None) -> int:
    """Run the command-line interface and return a process exit code."""
    args = list(sys.argv[1:] if argv is None else argv)

    if args:
        command = args[0]
        if command == "fetch" and len(args) >= 2:
            url = args[1]

            try:
                timeout = _parse_fetch_options(args[2:])
            except ValueError as error:
                print(f"Error: {error}", file=sys.stderr)
                return 2

            try:
                result = fetch_url(url, timeout=timeout)
            except (OSError, ValueError) as error:
                print(f"Error: could not fetch {url}: {error}", file=sys.stderr)
                return 1

            print(f"{result.status_code} {result.reason}")
            print(f"bytes: {len(result.body)}")
            return 0

        if command == "scrape" and len(args) >= 2:
            url = args[1]

            try:
                max_pages, output_path, timeout = _parse_scrape_options(args[2:])
            except ValueError as error:
                print(f"Error: {error}", file=sys.stderr)
                return 2

            try:
                records = scrape_pages(url, max_pages=max_pages, timeout=timeout)
            except (OSError, ValueError) as error:
                print(f"Error: could not scrape {url}: {error}", file=sys.stderr)
                return 1

            if output_path is not None:
                try:
                    count = write_records(records, output_path)
                except ValueError as error:
                    print(f"Error: {error}", file=sys.stderr)
                    return 2

                print(f"Wrote {count} records to {output_path}")
                return 0

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
            except (OSError, ValueError) as error:
                print(f"Error: {error}", file=sys.stderr)
                return 1

            if len(args) == 4 and args[2] == "--output":
                try:
                    count = write_records(records, args[3])
                except ValueError as error:
                    print(f"Error: {error}", file=sys.stderr)
                    return 2

                print(f"Wrote {count} records to {args[3]}")
                return 0

            if len(args) == 2:
                print(json.dumps(records))
                return 0

        usage = (
            "Usage: python -m public_directory_scraper "
            "[fetch URL [--timeout SECONDS] | "
            "scrape URL [--pages N] [--timeout SECONDS] "
            "[--output OUTPUT.csv|OUTPUT.xlsx] | "
            "parse HTML_FILE [--output OUTPUT.csv|OUTPUT.xlsx]]"
        )
        print(usage, file=sys.stderr)
        return 2

    print(f"public-directory-scraper {__version__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
