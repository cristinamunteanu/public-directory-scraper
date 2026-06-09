import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .exporter import write_records
from .fetcher import fetch_url
from .parser import parse_listings
from .scraper import scrape_pages


class _CliArgumentParser(argparse.ArgumentParser):
    """ArgumentParser variant that lets main return exit codes."""

    def error(self, message):
        """Raise an error instead of exiting the process."""
        raise ValueError(message)


def _parse_positive_float(value, option_name):
    """Parse a positive floating-point option value."""
    try:
        number = float(value)
    except ValueError as error:
        raise ValueError(f"{option_name} must be a positive number") from error

    if number <= 0:
        raise ValueError(f"{option_name} must be a positive number")

    return number


def _parse_non_negative_float(value, option_name):
    """Parse a non-negative floating-point option value."""
    try:
        number = float(value)
    except ValueError as error:
        raise ValueError(f"{option_name} must be zero or a positive number") from error

    if number < 0:
        raise ValueError(f"{option_name} must be zero or a positive number")

    return number


def _parse_non_negative_int(value, option_name):
    """Parse a non-negative integer option value."""
    try:
        number = int(value)
    except ValueError as error:
        raise ValueError(f"{option_name} must be zero or a positive integer") from error

    if number < 0:
        raise ValueError(f"{option_name} must be zero or a positive integer")

    return number


def _parse_positive_int(value, option_name):
    """Parse a positive integer option value."""
    try:
        number = int(value)
    except ValueError as error:
        raise ValueError(f"{option_name} must be a positive integer") from error

    if number < 1:
        raise ValueError(f"{option_name} must be a positive integer")

    return number


def _build_parser():
    """Build the command-line argument parser."""
    parser = _CliArgumentParser(prog="python -m public_directory_scraper")
    subparsers = parser.add_subparsers(dest="command")

    fetch_parser = subparsers.add_parser("fetch")
    fetch_parser.add_argument("url")
    fetch_parser.add_argument("--timeout", default="10")
    fetch_parser.add_argument("--retries", default="0")

    scrape_parser = subparsers.add_parser("scrape")
    scrape_parser.add_argument("url")
    scrape_parser.add_argument("--pages", default="1")
    scrape_parser.add_argument("--timeout", default="10")
    scrape_parser.add_argument("--retries", default="0")
    scrape_parser.add_argument("--delay", default="0")
    scrape_parser.add_argument("--output")

    parse_parser = subparsers.add_parser("parse")
    parse_parser.add_argument("input_path")
    parse_parser.add_argument("--output")

    return parser


def _parse_args(args):
    """Parse command-line arguments into a command namespace."""
    parser = _build_parser()
    return parser.parse_args(args)


def main(argv=None) -> int:
    """Run the command-line interface and return a process exit code."""
    args = list(sys.argv[1:] if argv is None else argv)

    if not args:
        print(f"public-directory-scraper {__version__}")
        return 0

    try:
        parsed_args = _parse_args(args)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2

    if parsed_args.command == "fetch":
        url = parsed_args.url

        try:
            timeout = _parse_positive_float(parsed_args.timeout, "--timeout")
            retries = _parse_non_negative_int(parsed_args.retries, "--retries")
        except ValueError as error:
            print(f"Error: {error}", file=sys.stderr)
            return 2

        try:
            result = fetch_url(url, timeout=timeout, retries=retries)
        except (OSError, ValueError) as error:
            print(f"Error: could not fetch {url}: {error}", file=sys.stderr)
            return 1

        print(f"{result.status_code} {result.reason}")
        print(f"bytes: {len(result.body)}")
        return 0

    if parsed_args.command == "scrape":
        url = parsed_args.url

        try:
            max_pages = _parse_positive_int(parsed_args.pages, "--pages")
            timeout = _parse_positive_float(parsed_args.timeout, "--timeout")
            delay = _parse_non_negative_float(parsed_args.delay, "--delay")
            retries = _parse_non_negative_int(parsed_args.retries, "--retries")
        except ValueError as error:
            print(f"Error: {error}", file=sys.stderr)
            return 2

        try:
            records = scrape_pages(
                url,
                max_pages=max_pages,
                timeout=timeout,
                delay=delay,
                retries=retries,
            )
        except (OSError, ValueError) as error:
            print(f"Error: could not scrape {url}: {error}", file=sys.stderr)
            return 1

        if parsed_args.output is not None:
            try:
                count = write_records(records, parsed_args.output)
            except ValueError as error:
                print(f"Error: {error}", file=sys.stderr)
                return 2
            except OSError as error:
                print(
                    f"Error: could not write {parsed_args.output}: {error}",
                    file=sys.stderr,
                )
                return 1

            print(f"Wrote {count} records to {parsed_args.output}")
            return 0

        print(json.dumps(records))
        return 0

    if parsed_args.command == "parse":
        input_path = parsed_args.input_path

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

        if parsed_args.output is not None:
            try:
                count = write_records(records, parsed_args.output)
            except ValueError as error:
                print(f"Error: {error}", file=sys.stderr)
                return 2
            except OSError as error:
                print(
                    f"Error: could not write {parsed_args.output}: {error}",
                    file=sys.stderr,
                )
                return 1

            print(f"Wrote {count} records to {parsed_args.output}")
            return 0

        print(json.dumps(records))
        return 0

    print(f"Error: unknown command: {parsed_args.command}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
