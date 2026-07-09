from pathlib import Path

from taro.scraper import parse_democracy_index_html

# Local copy of the currently-pinned oldid's page (see DEMOCRACY_INDEX_URL in
# scraper.py) - keeps this test fast, deterministic, and immune to
# Wikipedia's anti-bot blocking, since it never makes a network call.
# Regenerate this file whenever DEMOCRACY_INDEX_URL is re-pinned to a newer
# revision, e.g.:
#   curl -A "taro-arms-tracker/1.0" "<new DEMOCRACY_INDEX_URL>" \
#       -o tests/fixtures/democracy_index.html
FIXTURE_PATH = Path(__file__).parent / "fixtures" / "democracy_index.html"

EXPECTED_COLUMNS = [
    "Country", "Regime type", "2022", "2021", "2020", "2019", "2018",
    "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010",
    "2008", "2006",
]


def test_parse_democracy_index_html_shape():
    html = FIXTURE_PATH.read_bytes()
    table = parse_democracy_index_html(html)

    # One row per country - a row silently going missing (e.g. the
    # region-rowspan bug this used to have) wouldn't raise an error, so this
    # is checking for exactly that failure mode, not just "it ran".
    assert len(table) == 167
    assert all(list(row.keys()) == EXPECTED_COLUMNS for row in table)


def test_parse_democracy_index_html_values():
    html = FIXTURE_PATH.read_bytes()
    table = parse_democracy_index_html(html)

    # A shape/column check alone wouldn't catch columns being correctly
    # named but misaligned with the wrong values - spot-check one known row.
    canada = next(row for row in table if row["Country"] == "Canada")
    assert canada["Regime type"] == "Full democracy"
    assert canada["2022"] == 8.88
    assert canada["2006"] == 9.07
