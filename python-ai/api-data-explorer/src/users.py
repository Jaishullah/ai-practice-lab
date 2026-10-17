"""
users.py - RandomUser API: generate placeholder players for testing.

Flow:  generate_users()  ->  list of user objects  ->  build_squad_df()  ->  table
"""

from __future__ import annotations

import pandas as pd
from randomuser import RandomUser


def build_squad_df(users: list) -> pd.DataFrame:
    """Turn user objects into a table. Works with any object that has get_*() methods."""
    rows = [
        {
            "Name": user.get_full_name(),
            "Gender": user.get_gender(),
            "City": user.get_city(),
            "State": user.get_state(),
            "Email": user.get_email(),
            "DOB": user.get_dob(),
            "Picture": user.get_picture(),
        }
        for user in users
    ]
    return pd.DataFrame(rows)


def get_squad(size: int = 10) -> pd.DataFrame:
    """Call the RandomUser API and return `size` placeholder players as a table."""
    users = RandomUser.generate_users(size)  # <- the API request happens here
    return build_squad_df(users)
