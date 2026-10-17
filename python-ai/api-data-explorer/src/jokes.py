"""
jokes.py - Official Joke API: fun lines for the dressing room.

Flow:  fetch_jokes()  ->  list of dicts  ->  jokes_to_df()  ->  clean table
"""

from __future__ import annotations

import pandas as pd
import requests

JOKES_URL = "https://official-joke-api.appspot.com/jokes/ten"
TIMEOUT = 10


def fetch_jokes() -> list[dict]:
    """GET 10 random jokes as JSON."""
    response = requests.get(JOKES_URL, timeout=TIMEOUT)  # <- request / response
    response.raise_for_status()
    return response.json()


def jokes_to_df(results: list[dict]) -> pd.DataFrame:
    """Make a table and drop the columns we don't need (type, id)."""
    return pd.DataFrame(results).drop(columns=["type", "id"], errors="ignore")
