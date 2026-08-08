import os

import pandas as pd
import pytest

from taro.pipeline import (
    arms_pipeline,
    armed_conflicts_belligerents_pipeline,
    armed_conflicts_pipeline,
    country_name_pipeline,
    democracy_index_pipeline,
    export_data_pipeline,
    import_data_pipeline,
    peace_index_pipe,
)

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures", "peace_index")
ARMS_FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures", "arms")
DEMOCRACY_INDEX_FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures", "democracy_index")

# import_data_pipeline/export_data_pipeline read the same arms.csv shape
# arms_pipeline does (all three are sourced from arms.csv in __main__ too) -
# reusing that fixture rather than duplicating it.
COUNTRY_NAMES_FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures", "country_names")
ARMED_CONFLICTS_FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures", "armed_conflicts")


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


def test_democracy_index_pipeline_writes_expected_table(sqlite_conn):
    democracy_index_pipeline(
        source="csv",
        dest="postgres",
        csv_path=os.path.join(DEMOCRACY_INDEX_FIXTURES, "democracy_index.csv"),
        db_conn=sqlite_conn,
    )

    result = pd.read_sql("select * from democracy_index", sqlite_conn).set_index("Alpha-2 code")

    assert sorted(result.index) == ["AF", "AU"]
    assert result.loc["AF", "Regime type"] == "Authoritarian"
    assert result.loc["AU", "2025"] == 8.85


def test_democracy_index_pipeline_requires_csv_path():
    with pytest.raises(TypeError):
        democracy_index_pipeline(source="csv", dest="postgres", db_conn=None)


def test_import_data_pipeline_writes_expected_table(sqlite_conn):
    import_data_pipeline(
        source="csv",
        dest="postgres",
        csv_path=os.path.join(ARMS_FIXTURES, "arms.csv"),
        db_conn=sqlite_conn,
    )

    result = pd.read_sql("select * from imports", sqlite_conn)

    assert len(result) == 3
    assert result.loc[result["Source country"] == "FR", "EUR"].iloc[0] == 1000000


def test_import_data_pipeline_requires_csv_path():
    with pytest.raises(TypeError):
        import_data_pipeline(source="csv", dest="postgres", db_conn=None)


def test_export_data_pipeline_writes_expected_table(sqlite_conn):
    export_data_pipeline(
        source="csv",
        dest="postgres",
        csv_path=os.path.join(ARMS_FIXTURES, "arms.csv"),
        db_conn=sqlite_conn,
    )

    result = pd.read_sql("select * from exports", sqlite_conn)

    assert len(result) == 3
    assert result.loc[result["Source country"] == "FR", "EUR"].iloc[0] == 1000000


def test_export_data_pipeline_requires_csv_path():
    with pytest.raises(TypeError):
        export_data_pipeline(source="csv", dest="postgres", db_conn=None)


def test_country_name_pipeline_writes_expected_table(sqlite_conn):
    country_name_pipeline(
        source="csv",
        dest="postgres",
        csv_path=os.path.join(COUNTRY_NAMES_FIXTURES, "countries_info.csv"),
        db_conn=sqlite_conn,
    )

    result = pd.read_sql("select * from country_names", sqlite_conn)

    assert sorted(result["Alpha-2 code"]) == ["AF", "AL"]
    assert result.loc[result["Alpha-2 code"] == "AF", "short_name"].iloc[0] == "Afghanistan"
    assert result.loc[result["Alpha-2 code"] == "AL", "Alpha-3 code"].iloc[0] == "ALB"


def test_country_name_pipeline_requires_csv_path():
    with pytest.raises(TypeError):
        country_name_pipeline(source="csv", dest="postgres", db_conn=None)


def test_armed_conflicts_pipeline_writes_expected_table(sqlite_conn):
    armed_conflicts_pipeline(
        source="csv",
        dest="postgres",
        csv_path=os.path.join(ARMED_CONFLICTS_FIXTURES, "armed_conflicts.csv"),
        db_conn=sqlite_conn,
    )

    result = pd.read_sql("select * from armed_conflicts", sqlite_conn).set_index("conflict_id")

    assert sorted(result.index) == [1, 3]
    assert result.loc[1, "name"] == "Arab-Israeli / Iran-Israel conflict"
    assert result.loc[3, "total_deaths_est"] == 1600000
    assert result.loc[1, "confidence"] == "low"


def test_armed_conflicts_pipeline_requires_csv_path():
    with pytest.raises(TypeError):
        armed_conflicts_pipeline(source="csv", dest="postgres", db_conn=None)


def test_armed_conflicts_belligerents_pipeline_writes_expected_table(sqlite_conn):
    armed_conflicts_belligerents_pipeline(
        source="csv",
        dest="postgres",
        csv_path=os.path.join(ARMED_CONFLICTS_FIXTURES, "armed_conflicts_belligerents.csv"),
        db_conn=sqlite_conn,
    )

    result = pd.read_sql("select * from armed_conflicts_belligerents", sqlite_conn)

    assert "index" not in result.columns
    assert len(result) == 6
    assert sorted(result.loc[result["conflict_id"] == 1, "Alpha-2 code"]) == ["EG", "IL", "PS"]


def test_armed_conflicts_belligerents_pipeline_requires_csv_path():
    with pytest.raises(TypeError):
        armed_conflicts_belligerents_pipeline(source="csv", dest="postgres", db_conn=None)
