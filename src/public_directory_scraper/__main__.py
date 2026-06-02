from . import __version__


def main() -> int:
    print(f"public-directory-scraper {__version__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
