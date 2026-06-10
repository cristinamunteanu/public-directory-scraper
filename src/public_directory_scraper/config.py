import os
from dataclasses import dataclass


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
