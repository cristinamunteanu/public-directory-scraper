import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EtlConfig:
    """Configuration values needed by the future ETL pipeline."""

    database_url: str
    default_pages: int = 1
    default_timeout: float = 10
    default_retries: int = 0
    default_delay: float = 0


def load_config(environ=None):
    """Load ETL configuration from environment variables."""
    values = os.environ if environ is None else environ
    database_url = values.get("DATABASE_URL", "").strip()

    if not database_url:
        raise ValueError("DATABASE_URL is required")

    return EtlConfig(
        database_url=database_url,
        default_pages=_get_number(
            values,
            "DEFAULT_PAGES",
            1,
            int,
            1,
            "a positive integer",
        ),
        default_timeout=_get_number(
            values,
            "DEFAULT_TIMEOUT",
            10,
            float,
            0,
            "a positive number",
            include_minimum=False,
        ),
        default_retries=_get_number(
            values,
            "DEFAULT_RETRIES",
            0,
            int,
            0,
            "zero or a positive integer",
        ),
        default_delay=_get_number(
            values,
            "DEFAULT_DELAY",
            0,
            float,
            0,
            "zero or a positive number",
        ),
    )


def load_env_file(path=".env", environ=None):
    """Load simple KEY=value settings from a local .env file."""
    values = os.environ if environ is None else environ
    env_path = Path(path)

    try:
        lines = env_path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return 0

    loaded_count = 0

    for line_number, line in enumerate(lines, start=1):
        text = line.strip()

        if not text or text.startswith("#"):
            continue

        if "=" not in text:
            raise ValueError(f"invalid .env line {line_number}: expected KEY=value")

        name, value = text.split("=", 1)
        name = name.strip()

        if not name:
            raise ValueError(f"invalid .env line {line_number}: expected KEY=value")

        if name in values:
            continue

        values[name] = _strip_optional_quotes(value.strip())
        loaded_count += 1

    return loaded_count


def _get_number(
    values,
    name,
    default,
    convert,
    minimum,
    description,
    include_minimum=True,
):
    """Read a numeric environment value and validate its lower bound."""
    raw_value = values.get(name, str(default))

    try:
        value = convert(raw_value)
    except ValueError as error:
        raise ValueError(f"{name} must be {description}") from error

    if value < minimum or (not include_minimum and value == minimum):
        raise ValueError(f"{name} must be {description}")

    return value


def _strip_optional_quotes(value):
    """Remove matching single or double quotes around an environment value."""
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]

    return value
