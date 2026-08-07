import os

import pandas as pd
import pytest

from taro.pipeline import peace_index_pipe

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures", "peace_index")


def test_peace_index_pipe_writes_expected_table(sqlite_conn):
    peace_index_pipe(
        source="csv",
        dest="postgres",
        csv_path=os.path.join(FIXTURES, "gpi_scores.csv"),
        codes_csv_path=os.path.join(FIXTURES, "countries_info.csv"),
        db_conn=sqlite_conn,
    )

    result = pd.read_sql("select * from peace_index", sqlite_conn).set_index("Alpha-2 code")

    # "Nowhereland" (in the GPI file, no matching codes entry) and "Atlantis"
    # (in the codes file, no matching GPI entry) are both dropped by the
    # inner-join merge rather than appearing with nulls.
    assert sorted(result.index) == ["AF", "AL"]
    assert list(result.columns) == [str(year) for year in range(2008, 2023)]
    assert result.loc["AF", "2008"] == 3.095
    assert result.loc["AL", "2022"] == 1.761


def test_peace_index_pipe_requires_csv_path():
    with pytest.raises(TypeError):
        peace_index_pipe(source="csv", dest="postgres", codes_csv_path="x", db_conn=None)


def test_peace_index_pipe_requires_codes_csv_path():
    with pytest.raises(TypeError):
        peace_index_pipe(source="csv", dest="postgres", csv_path="x", db_conn=None)
