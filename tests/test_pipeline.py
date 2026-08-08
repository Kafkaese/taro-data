import os

import pandas as pd
import pytest

from taro.pipeline import arms_pipeline, peace_index_pipe

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures", "peace_index")
ARMS_FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures", "arms")


def test_peace_index_pipe_writes_expected_table(sqlite_conn):
    peace_index_pipe(
        source="csv",
        dest="postgres",
        csv_path=os.path.join(FIXTURES, "gpi_scores.csv"),
        db_conn=sqlite_conn,
    )

    result = pd.read_sql("select * from peace_index", sqlite_conn).set_index("Alpha-2 code")

    assert sorted(result.index) == ["AF", "AL"]
    assert list(result.columns) == [str(year) for year in range(2008, 2023)]
    assert result.loc["AF", "2008"] == 3.095
    assert result.loc["AL", "2022"] == 1.761


def test_peace_index_pipe_requires_csv_path():
    with pytest.raises(TypeError):
        peace_index_pipe(source="csv", dest="postgres", db_conn=None)


def test_arms_pipeline_writes_expected_table(sqlite_conn):
    arms_pipeline(
        source="csv",
        dest="postgres",
        csv_path=os.path.join(ARMS_FIXTURES, "arms.csv"),
        db_conn=sqlite_conn,
    )

    result = pd.read_sql("select * from arms", sqlite_conn)

    assert len(result) == 3
    assert result["Year"].tolist() == [1999, 1999, 2000]
    assert result.loc[result["Source country"] == "FR", "EUR"].iloc[0] == 1000000
