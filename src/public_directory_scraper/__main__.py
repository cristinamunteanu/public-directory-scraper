import json
import sys
from pathlib import Path

from . import __version__
from .parser import parse_listing


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)

    if args:
        command = args[0]
        if command == "parse" and len(args) == 2:
            html = Path(args[1]).read_text(encoding="utf-8")
            print(json.dumps(parse_listing(html)))
            return 0

        print("Usage: python -m public_directory_scraper [parse HTML_FILE]", file=sys.stderr)
        return 2

    print(f"public-directory-scraper {__version__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
