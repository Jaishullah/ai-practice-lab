"""Run the full India vs Afghanistan analysis: python main.py"""

from src.analysis import plot_run_difference, split_by_venue, summarize
from src.cricket_api import get_matches, get_team_id, get_teams_df


def main() -> None:
    teams = get_teams_df()
    print("Teams:\n", teams, "\n")
    print("India id:", get_team_id(teams, "India"), "| Afghanistan id:", get_team_id(teams, "Afghanistan"))

    matches = get_matches()
    print("\nFirst matches:\n", matches.head(), "\n")

    home, neutral = split_by_venue(matches)
    print(f"Average run difference at home:    {home['RUN_DIFF'].mean():.1f}")
    print(f"Average run difference at neutral: {neutral['RUN_DIFF'].mean():.1f}")

    print("\nSummary by venue type:\n", summarize(matches))

    # Quiz from the original lab: mean runs scored by India
    print(f"\nIndia mean runs (home):    {home['IND_RUNS'].mean():.1f}")
    print(f"India mean runs (neutral): {neutral['IND_RUNS'].mean():.1f}")

    chart = plot_run_difference(matches, "docs/run_difference.png")
    print("\nChart saved to", chart)


if __name__ == "__main__":
    main()
