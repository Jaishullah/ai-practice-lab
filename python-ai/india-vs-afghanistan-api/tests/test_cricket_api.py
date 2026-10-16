import pytest

from src.analysis import split_by_venue
from src.cricket_api import get_matches, get_team_id, get_teams_df, merge_dicts


def test_merge_dicts():
    assert merge_dicts([{"a": 1}, {"a": 2}]) == {"a": [1, 2]}


def test_team_lookup():
    teams = get_teams_df()
    assert get_team_id(teams, "India") == 1
    with pytest.raises(ValueError):
        get_team_id(teams, "Narnia")


def test_run_diff_and_split():
    matches = get_matches()
    assert (matches["RUN_DIFF"] == matches["IND_RUNS"] - matches["AFG_RUNS"]).all()
    home, neutral = split_by_venue(matches)
    assert len(home) + len(neutral) == len(matches)
