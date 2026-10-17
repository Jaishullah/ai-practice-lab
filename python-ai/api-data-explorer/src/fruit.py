"""
fruit.py - Fruityvice API: nutrition data for a player's diet plan.

Flow:  fetch_fruit_data()  ->  list of nested dicts  ->  fruits_to_df()  ->  flat table
"""

from __future__ import annotations

import pandas as pd
import requests

FRUIT_URL = "https://fruityvice.com/api/fruit/all"
TIMEOUT = 10


def fetch_fruit_data() -> list[dict]:
    """GET all fruits. Returns the JSON as a Python list of dictionaries."""
    response = requests.get(FRUIT_URL, timeout=TIMEOUT)  # <- request / response
    response.raise_for_status()
    return response.json()  # same result as json.loads(response.text)


def fruits_to_df(results: list[dict]) -> pd.DataFrame:
    """Flatten nested JSON: {'nutritions': {'calories': 96}} -> column 'nutritions.calories'."""
    return pd.json_normalize(results)


def _find_fruit(df: pd.DataFrame, name: str) -> pd.Series:
    match = df.loc[df["name"] == name]
    if match.empty:
        raise ValueError(f"Fruit not found: {name!r}")
    return match.iloc[0]


def get_family_and_genus(df: pd.DataFrame, name: str) -> tuple[str, str]:
    """Example: ('Rosaceae', 'Prunus') for Cherry."""
    row = _find_fruit(df, name)
    return row["family"], row["genus"]


def get_calories(df: pd.DataFrame, name: str) -> float:
    """Calories for one fruit, for example Banana."""
    return _find_fruit(df, name)["nutritions.calories"]
