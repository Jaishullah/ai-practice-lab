"""analysis.py - statistics and chart for India vs Afghanistan."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # lets the script run without a display
import matplotlib.pyplot as plt
import pandas as pd


def split_by_venue(matches: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (home_matches, neutral_matches) for India."""
    home = matches[matches["VENUE_TYPE"] == "Home"]
    neutral = matches[matches["VENUE_TYPE"] == "Neutral"]
    return home, neutral


def summarize(matches: pd.DataFrame) -> pd.DataFrame:
    """Average runs and average run difference, grouped by venue type."""
    return (
        matches.groupby("VENUE_TYPE")[["IND_RUNS", "AFG_RUNS", "RUN_DIFF"]]
        .mean()
        .round(1)
    )


def plot_run_difference(matches: pd.DataFrame, output: Path | str) -> Path:
    """Save a line chart of run difference over time, split by venue type."""
    home, neutral = split_by_venue(matches)
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(home["MATCH_DATE"], home["RUN_DIFF"], marker="o", label="Home")
    ax.plot(neutral["MATCH_DATE"], neutral["RUN_DIFF"], marker="s", label="Neutral")
    ax.axhline(0, color="grey", linestyle="--", linewidth=1)
    ax.set_title("India vs Afghanistan: run difference over time (sample data)")
    ax.set_xlabel("Match date")
    ax.set_ylabel("India runs - Afghanistan runs")
    ax.legend()
    fig.tight_layout()
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=150)
    plt.close(fig)
    return output
