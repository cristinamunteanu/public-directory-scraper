def connect(database_url, connector=None):
    """Open a Postgres connection for the ETL pipeline."""
    if not database_url:
        raise ValueError("database_url is required")

    connect_function = connector or _load_psycopg_connect()
    return connect_function(database_url)


def _load_psycopg_connect():
    """Load psycopg's connect function when a real connection is needed."""
    from psycopg import connect as psycopg_connect

    return psycopg_connect
