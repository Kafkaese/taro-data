# Pure unit tests: no live Postgres, no seeded data, no network. `db` is
# swapped out for a mock in every test that reaches the database, so these
# only assert on the API layer's own behavior (request validation, response
# shaping, error fallbacks) - not on any particular dataset's real values.
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from api.country_data_api import app

client = TestClient(app)


@pytest.fixture
def mock_conn(monkeypatch):
    """Replaces the module-level `db` engine with a mock and returns the
    connection it hands out, so a test can just set `mock_conn.execute
    .return_value.fetchall.return_value` to whatever rows it wants."""
    conn = MagicMock()
    db = MagicMock()
    db.connect.return_value.__enter__.return_value = conn
    monkeypatch.setattr("api.country_data_api.db", db)
    return conn


def rows(*rows):
    """Small helper: wire a mock connection to return these rows from
    whatever query is executed against it."""
    def _apply(conn):
        conn.execute.return_value.fetchall.return_value = list(rows)
    return _apply


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"status": 200}


@pytest.mark.parametrize("endpoint, params", [
    ("/metadata/name/short", {}),
    ("/metadata/democracy_index", {"country_code": "CA"}),
    ("/metadata/peace_index", {"country_code": "CA"}),
    ("/arms/exports/total", {"country_code": "CA", "year": 2020}),
    ("/arms/exports/timeseries", {"country_code": "CA"}),
    ("/arms/exports/by_country", {"country_code": "CA", "year": 2020}),
    ("/arms/exports/available", {}),
    ("/arms/imports/total", {"country_code": "CA", "year": 2020}),
    ("/arms/imports/by_country", {"country_code": "CA", "year": 2020}),
    ("/arms/imports/timeseries", {"country_code": "CA"}),
    ("/arms/imports/available", {}),
])
def test_missing_required_param_is_422(endpoint, params):
    response = client.get(endpoint, params=params)

    assert response.status_code == 422


@pytest.mark.parametrize("endpoint", [
    "/arms/exports/total",
    "/arms/exports/timeseries",
    "/arms/exports/by_country",
    "/arms/imports/total",
    "/arms/imports/by_country",
    "/arms/imports/timeseries",
])
def test_invalid_currency_returns_no_data(endpoint, mock_conn):
    response = client.get(endpoint, params={
        "country_code": "CA", "year": 2020, "currency": "GBP",
    })

    assert response.status_code == 200
    assert response.json() == {"value": "no data"}
    mock_conn.execute.assert_not_called()


@pytest.mark.parametrize("endpoint", [
    "/metadata/democracy_index",
    "/metadata/peace_index",
])
@pytest.mark.parametrize("year", [
    "abc",
    "2020; DROP TABLE peace_index;--",
    '2020" --',
    "202",
    "20200",
])
def test_malformed_year_returns_no_data_without_querying(endpoint, year, mock_conn):
    # `year` gets spliced into these two queries as a column identifier
    # (SQLAlchemy can't bind identifiers as parameters) - anything that
    # isn't exactly 4 digits must be rejected before it ever reaches the
    # query string.
    response = client.get(endpoint, params={"country_code": "CA", "year": year})

    assert response.status_code == 200
    assert response.json() == {"value": "no data"}
    mock_conn.execute.assert_not_called()


@pytest.mark.parametrize("endpoint, params", [
    ("/metadata/name/short", {"country_code": "XX"}),
    ("/metadata/democracy_index", {"country_code": "XX", "year": 2020}),
    ("/metadata/peace_index", {"country_code": "XX", "year": 2020}),
    ("/arms/exports/by_country", {"country_code": "XX", "year": 2020, "currency": "EUR"}),
    ("/arms/imports/by_country", {"country_code": "XX", "year": 2020, "currency": "EUR"}),
    ("/arms/exports/timeseries", {"country_code": "XX", "currency": "EUR"}),
    ("/arms/imports/timeseries", {"country_code": "XX", "currency": "EUR"}),
])
def test_empty_result_returns_no_data(endpoint, params, mock_conn):
    rows()(mock_conn)

    response = client.get(endpoint, params=params)

    assert response.status_code == 200
    assert response.json() == {"value": "no data"}


@pytest.mark.parametrize("endpoint, params", [
    ("/metadata/democracy_index", {"country_code": "CA", "year": 2020}),
    ("/metadata/peace_index", {"country_code": "CA", "year": 2020}),
])
def test_metadata_scalar_result(endpoint, params, mock_conn):
    rows((9.24,))(mock_conn)

    response = client.get(endpoint, params=params)

    assert response.status_code == 200
    assert response.json() == {"value": 9.24}


def test_arms_total_aggregate_null_falls_back_to_backup_query(mock_conn):
    # SUM() over zero matching rows comes back as a single (None,) row, not
    # an empty result - the handler queries the `exports` fallback table in
    # that case rather than treating it as "no data" immediately.
    mock_conn.execute.side_effect = [
        MagicMock(fetchall=MagicMock(return_value=[(None,)])),
        MagicMock(fetchall=MagicMock(return_value=[(500,)])),
    ]

    response = client.get("/arms/exports/total", params={
        "country_code": "CA", "year": 2020, "currency": "EUR",
    })

    assert response.status_code == 200
    assert response.json() == {"value": 500}
    assert mock_conn.execute.call_count == 2


@pytest.mark.parametrize("endpoint, params", [
    ("/arms/exports/timeseries", {"country_code": "CA", "currency": "EUR"}),
    ("/arms/imports/timeseries", {"country_code": "CA", "currency": "EUR"}),
])
def test_timeseries_shape(endpoint, params, mock_conn):
    rows((2019, 100), (2020, 200))(mock_conn)

    response = client.get(endpoint, params=params)

    assert response.status_code == 200
    assert response.json() == [
        {"year": 2019, "value": 100},
        {"year": 2020, "value": 200},
    ]


@pytest.mark.parametrize("endpoint, params", [
    ("/arms/exports/by_country", {"country_code": "CA", "year": 2020, "currency": "EUR"}),
    ("/arms/imports/by_country", {"country_code": "CA", "year": 2020, "currency": "EUR"}),
])
def test_by_country_shape(endpoint, params, mock_conn):
    rows(("FR", 100, "France"), ("DE", 50, "Germany"))(mock_conn)

    response = client.get(endpoint, params=params)

    assert response.status_code == 200
    assert response.json() == [
        {"name": "FR", "value": 100, "full_name": "France"},
        {"name": "DE", "value": 50, "full_name": "Germany"},
    ]


@pytest.mark.parametrize("endpoint", [
    "/arms/exports/available",
    "/arms/imports/available",
])
def test_available_returns_bare_array_and_drops_nulls(endpoint, mock_conn):
    rows(("CA",), ("FR",), (None,))(mock_conn)

    response = client.get(endpoint, params={"year": 2020})

    assert response.status_code == 200
    assert response.json() == ["CA", "FR"]


@pytest.mark.parametrize("endpoint", [
    "/arms/exports/available",
    "/arms/imports/available",
])
def test_available_returns_empty_array_for_no_data(endpoint, mock_conn):
    rows()(mock_conn)

    response = client.get(endpoint, params={"year": 1778})

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.parametrize("endpoint, params, expected", [
    ("/metadata/name/short", {"country_code": "CA"}, {"value": "no data"}),
    ("/arms/exports/total", {"country_code": "CA", "year": 2020, "currency": "EUR"}, {"value": "no data"}),
    ("/arms/exports/available", {"year": 2020}, []),
    ("/arms/imports/available", {"year": 2020}, []),
])
def test_db_error_degrades_gracefully(endpoint, params, expected, mock_conn):
    # Every handler wraps its query in a bare try/except and returns a
    # sentinel rather than letting a DB error surface as a 500 - e.g. the
    # metadata endpoints hitting a year column that doesn't exist yet.
    mock_conn.execute.side_effect = Exception("boom")

    response = client.get(endpoint, params=params)

    assert response.status_code == 200
    assert response.json() == expected
