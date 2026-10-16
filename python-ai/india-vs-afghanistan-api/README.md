# India vs Afghanistan: Cricket Match Analysis with an API-Style Data Layer

A small Python project that shows how **APIs**, **JSON-like data** and **Pandas** work together,
using a cricket rivalry (India vs Afghanistan) as the example.

> **Data note:** `data/india_vs_afghanistan_sample.csv` is **illustrative sample data**, not official
> match records. Use `fetch_matches_from_api()` to plug in a real cricket data provider.

## What it does

| Step | Function | Idea |
|------|----------|------|
| 1 | `get_teams()` | Teams endpoint: returns a list of dictionaries (like JSON) |
| 2 | `merge_dicts()` / `get_teams_df()` | Convert that list into a Pandas table |
| 3 | `get_team_id()` | Find a team's unique ID by name |
| 4 | `get_matches()` | Load match data (offline CSV) |
| 5 | `fetch_matches_from_api()` | Template for a real REST call: request, JSON response, DataFrame |
| 6 | `split_by_venue()` / `summarize()` | Compare Home vs Neutral venues |
| 7 | `plot_run_difference()` | Save a chart to `docs/run_difference.png` |

`RUN_DIFF = India runs - Afghanistan runs`. Positive means India scored more.

## Project structure

```
.
├── main.py                  # runs the whole analysis
├── src/
│   ├── cricket_api.py       # data layer (teams, matches, REST template)
│   └── analysis.py          # statistics and chart
├── data/india_vs_afghanistan_sample.csv
├── tests/test_cricket_api.py
├── docs/run_difference.png  # generated chart
└── EXPLAINED.md             # beginner-friendly code walkthrough
```

## Run it

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
pytest
```

## Using a real API

```python
import os
from src.cricket_api import fetch_matches_from_api

matches = fetch_matches_from_api("https://your-provider.example/api", os.environ["CRICKET_API_KEY"])
```

Keep your key in an environment variable, never in the code.

## Limitation

Test matches have much larger totals than T20Is, which inflates the averages.
A good next step is to group by `FORMAT` as well.

## Tech stack

Python 3.10+, Pandas, Matplotlib, Requests, Pytest
