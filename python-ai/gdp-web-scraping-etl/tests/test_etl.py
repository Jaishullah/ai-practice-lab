"""Offline tests using small SAMPLE data (numbers are made up for testing)."""

import pandas as pd
import pytest

from src.etl import convert_to_billions, extract_table, load_to_csv, select_top_economies


def sample_table() -> pd.DataFrame:
    rows = [["World", "-", 1000000, "2023"]]  # first row = world total, must be skipped
    rows += [[f"Country {i}", "Region", 1_000_000 - i * 1000 + 0.5 * i, "2023"] for i in range(1, 13)]
    return pd.DataFrame(rows, columns=["Country", "Region", "GDP", "Year"])


def test_select_top_economies_shape_and_names():
    top = select_top_economies(sample_table())
    assert top.shape == (10, 2)
    assert list(top.columns) == ["Country", "GDP (Million USD)"]
    assert top.iloc[0]["Country"] == "Country 1"      # 'World' row was skipped
    assert top.iloc[-1]["Country"] == "Country 10"


def test_convert_to_billions_values_and_header():
    df = pd.DataFrame({"Country": ["A", "B"], "GDP (Million USD)": ["1,234,567", 26949643]})
    out = convert_to_billions(df)
    assert list(out.columns) == ["Country", "GDP (Billion USD)"]
    assert out["GDP (Billion USD)"].tolist() == [1234.57, 26949.64]


def test_convert_rejects_non_numbers():
    df = pd.DataFrame({"Country": ["A"], "GDP (Million USD)": ["n/a"]})
    with pytest.raises(ValueError):
        convert_to_billions(df)


def test_load_to_csv(tmp_path):
    df = pd.DataFrame({"Country": ["A"], "GDP (Billion USD)": [1.5]})
    path = load_to_csv(df, tmp_path / "sub" / "out.csv")
    assert pd.read_csv(path).equals(df)               # no extra index column


def test_extract_table_picks_right_table_from_html():
    html = "<table><tr><th>x</th></tr><tr><td>1</td></tr></table>" \
           "<table><tr><th>name</th></tr><tr><td>India</td></tr></table>"
    table = extract_table(html, table_index=1)
    assert table.iloc[0, 0] == "India"
    with pytest.raises(ValueError):
        extract_table(html, table_index=5)
