"""Offline tests: sample data replaces the real APIs."""

import pytest

from src.fruit import fruits_to_df, get_calories, get_family_and_genus
from src.jokes import jokes_to_df
from src.users import build_squad_df


class FakeUser:
    def __init__(self, name):
        self.name = name

    def get_full_name(self): return self.name
    def get_gender(self): return "male"
    def get_city(self): return "Kabul"
    def get_state(self): return "Kabul"
    def get_email(self): return f"{self.name.split()[0].lower()}@example.com"
    def get_dob(self): return "1995-01-01"
    def get_picture(self): return "http://example.com/pic.jpg"


FRUITS = [
    {"name": "Banana", "family": "Musaceae", "genus": "Musa", "nutritions": {"calories": 96}},
    {"name": "Cherry", "family": "Rosaceae", "genus": "Prunus", "nutritions": {"calories": 50}},
]


def test_squad_table_has_one_row_per_user():
    df = build_squad_df([FakeUser("Virat Sample"), FakeUser("Rashid Sample")])
    assert len(df) == 2
    assert list(df.columns) == ["Name", "Gender", "City", "State", "Email", "DOB", "Picture"]
    assert df.loc[0, "Email"] == "virat@example.com"


def test_json_normalize_flattens_nested_data():
    df = fruits_to_df(FRUITS)
    assert "nutritions.calories" in df.columns


def test_fruit_lookups():
    df = fruits_to_df(FRUITS)
    assert get_calories(df, "Banana") == 96
    assert get_family_and_genus(df, "Cherry") == ("Rosaceae", "Prunus")


def test_unknown_fruit_raises():
    with pytest.raises(ValueError):
        get_calories(fruits_to_df(FRUITS), "Durian")


def test_jokes_drop_type_and_id():
    jokes = [{"type": "general", "id": 1, "setup": "Why?", "punchline": "Because."}]
    df = jokes_to_df(jokes)
    assert list(df.columns) == ["setup", "punchline"]
