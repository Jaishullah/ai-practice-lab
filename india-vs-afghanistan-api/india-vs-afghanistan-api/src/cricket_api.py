"""
cricket_api.py
--------------
A tiny, API-style data layer for cricket match analysis.

It mirrors the structure of a real REST API client:
    teams endpoint   -> get_teams()
    matches endpoint -> get_matches() / fetch_matches_from_api()

By default it reads a local sample CSV so the project runs offline.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import requests

DEFAULT_DATA = Path(__file__).resolve().parent.parent / "data" / "india_vs_afghanistan_sample.csv"

# --- "Teams endpoint": a list of dictionaries, one per team ------------------
_TEAMS = [
    {"id": 1, "full_name": "India", "abbreviation": "IND", "nickname": "Men in Blue"},
    {"id": 2, "full_name": "Afghanistan", "abbreviation": "AFG", "nickname": "Afghan Atalan"},
    {"id": 3, "full_name": "Australia", "abbreviation": "AUS", "nickname": "Baggy Greens"},
    {"id": 4, "full_name": "England", "abbreviation": "ENG", "nickname": "Three Lions"},
]


def get_teams() -> list[dict]:
    """Return all teams, like a GET /teams call."""
    return [dict(team) for team in _TEAMS]


def merge_dicts(list_of_dicts: list[dict]) -> dict[str, list]:
    """Turn [{'id': 1, ...}, {'id': 2, ...}] into {'id': [1, 2], ...}."""
    merged = {key: [] for key in list_of_dicts[0]}
    for item in list_of_dicts:
        for key, value in item.items():
            merged[key].append(value)
    return merged


def get_teams_df() -> pd.DataFrame:
    """Teams as a table (one row per team)."""
    return pd.DataFrame(merge_dicts(get_teams()))


def get_team_id(teams_df: pd.DataFrame, full_name: str) -> int:
    """Look up a team's unique id by its full name."""
    row = teams_df[teams_df["full_name"] == full_name]
    if row.empty:
        raise ValueError(f"Team not found: {full_name!r}")
    return int(row["id"].iloc[0])


# --- "Matches endpoint" -------------------------------------------------------
def add_run_difference(matches: pd.DataFrame) -> pd.DataFrame:
    """
    Add RUN_DIFF = India runs - Afghanistan runs.
    Positive -> India scored more. Negative -> Afghanistan scored more.
    """
    matches = matches.copy()
    matches["MATCH_DATE"] = pd.to_datetime(matches["MATCH_DATE"])
    matches["RUN_DIFF"] = matches["IND_RUNS"] - matches["AFG_RUNS"]
    return matches.sort_values("MATCH_DATE").reset_index(drop=True)


def get_matches(path: Path | str = DEFAULT_DATA) -> pd.DataFrame:
    """Offline mode: load matches from a local CSV."""
    return add_run_difference(pd.read_csv(path))


def fetch_matches_from_api(base_url: str, api_key: str, timeout: int = 10) -> pd.DataFrame:
    """
    Online mode (template): request -> HTTP -> JSON response -> DataFrame.

    Point `base_url` at any cricket API that returns a JSON list of matches
    with the same columns as the sample CSV. Never hard-code `api_key`;
    read it from an environment variable.
    """
    response = requests.get(
        f"{base_url}/matches",
        params={"team1": "IND", "team2": "AFG"},
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=timeout,
    )
    response.raise_for_status()  # raises an error for 4xx / 5xx responses
    return add_run_difference(pd.DataFrame(response.json()))
