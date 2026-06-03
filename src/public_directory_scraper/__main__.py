import json
import sys
from pathlib import Path

from . import __version__
from .exporter import write_records_csv
from .parser import parse_listings


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)

    if args:
        command = args[0]
        if command == "parse" and len(args) in {2, 4}:
            html = Path(args[1]).read_text(encoding="utf-8")
            records = parse_listings(html)

            if len(args) == 4 and args[2] == "--output":
                count = write_records_csv(records, args[3])
                print(f"Wrote {count} records to {args[3]}")
                return 0

            if len(args) == 2:
                print(json.dumps(records))
                return 0

        usage = (
            "Usage: python -m public_directory_scraper "
            "[parse HTML_FILE [--output OUTPUT.csv]]"
        )
        print(usage, file=sys.stderr)
        return 2

    print(f"public-directory-scraper {__version__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
