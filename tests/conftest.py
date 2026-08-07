# country_data_api.py reads these via os.environ[...] at import time (to
# build its DB connection string and pick a CORS origin list) and raises
# KeyError if they're missing - set to harmless dummy values here so the
# module can be imported for testing without any real Postgres or AWS
# credentials. setdefault() so a real environment (e.g. running pytest
# inside the docker-compose dev stack) isn't overridden.
import os

os.environ.setdefault("ENV", "test")
os.environ.setdefault("POSTGRES_HOST", "localhost")
os.environ.setdefault("POSTGRES_PORT", "5432")
os.environ.setdefault("POSTGRES_DB", "test")
os.environ.setdefault("POSTGRES_USER", "test")
os.environ.setdefault("POSTGRES_PASSWORD", "test")

import pytest
from sqlalchemy import create_engine


@pytest.fixture
def sqlite_conn():
    """An in-memory SQLite connection standing in for a Postgres `db_conn` in
    pipeline tests - exercises the same pandas to_sql/read_sql path the real
    pipelines use, without needing a live database."""
    with create_engine("sqlite:///:memory:").connect() as conn:
        yield conn
