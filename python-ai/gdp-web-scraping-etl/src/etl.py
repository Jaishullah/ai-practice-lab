"""
etl.py - A tiny ETL pipeline: top 10 economies by GDP (IMF figures).

    EXTRACT    extract_table()           web page  -> raw table
    TRANSFORM  select_top_economies()    raw table -> 2 columns, 10 rows
               convert_to_billions()     million USD -> billion USD, rounded
    LOAD       load_to_csv()             clean table -> CSV file
    run_pipeline() chains all of the above.
"""

from __future__ import annotations

from io import StringIO
from pathlib import Path

import numpy as np
import pandas as pd
import requests

URL = (
    "https://web.archive.org/web/20230902185326/"
    "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
)
TABLE_INDEX = 3  # the IMF table is the 4th table on the page (counting from 0)
TIMEOUT = 30
HEADERS = {"User-Agent": "Mozilla/5.0 (learning project)"}  # some sites reject unknown clients


# ----------------------------- EXTRACT --------------------------------------
def extract_table(source: str = URL, table_index: int = TABLE_INDEX) -> pd.DataFrame:
    """Download a web page and return one of its HTML tables as a DataFrame."""
    if source.startswith("http"):
        response = requests.get(source, headers=HEADERS, timeout=TIMEOUT)  # request / response
        response.raise_for_status()
        html = response.text
    else:
        html = source  # lets tests pass raw HTML instead of a URL
    tables = pd.read_html(StringIO(html))  # finds every <table> on the page
    if table_index >= len(tables):
        raise ValueError(f"Page has only {len(tables)} tables, wanted index {table_index}")
    return tables[table_index]


# ----------------------------- TRANSFORM ------------------------------------
def select_top_economies(table: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Keep the country and IMF GDP columns, and the top_n rows (skipping the 'World' row)."""
    df = table.copy()
    df.columns = range(df.shape[1])          # replace messy multi-level headers with 0, 1, 2 ...
    df = df[[0, 2]]                          # column 0 = country, column 2 = IMF GDP (million USD)
    df = df.iloc[1 : top_n + 1, :]           # row 0 is the world total, so start at row 1
    df.columns = ["Country", "GDP (Million USD)"]
    return df.reset_index(drop=True)


def convert_to_billions(df: pd.DataFrame) -> pd.DataFrame:
    """Convert GDP from million USD to billion USD, rounded to 2 decimals."""
    df = df.copy()
    cleaned = df["GDP (Million USD)"].astype(str).str.replace(",", "", regex=False)
    numbers = pd.to_numeric(cleaned, errors="coerce")
    if numbers.isna().any():
        bad = df.loc[numbers.isna(), "Country"].tolist()
        raise ValueError(f"GDP is not a number for: {bad}")
    df["GDP (Million USD)"] = np.round(numbers / 1000, 2)   # 1 billion = 1000 million
    return df.rename(columns={"GDP (Million USD)": "GDP (Billion USD)"})  # must be assigned!


# ------------------------------- LOAD ---------------------------------------
def load_to_csv(df: pd.DataFrame, path: Path | str = "output/Largest_economies.csv") -> Path:
    """Save the table to a CSV file (without the 0,1,2... row numbers)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path


# ------------------------------ PIPELINE ------------------------------------
def run_pipeline(source: str = URL, output: Path | str = "output/Largest_economies.csv") -> pd.DataFrame:
    raw = extract_table(source)                # E
    top = select_top_economies(raw)            # T (step 1)
    final = convert_to_billions(top)           # T (step 2)
    load_to_csv(final, output)                 # L
    return final
