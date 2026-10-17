# API Data Explorer

A small Python lab that loads data from **three public APIs** and turns it into clean
Pandas tables, using a cricket-team theme.

| API | Library | Cricket theme | What it shows |
|---|---|---|---|
| [RandomUser](https://randomuser.me) | `randomuser` | Placeholder squad of players | Using an API wrapper library |
| [Fruityvice](https://www.fruityvice.com) | `requests` | Diet plan nutrition (banana calories) | Nested JSON flattened with `json_normalize` |
| [Official Joke API](https://official-joke-api.appspot.com) | `requests` | Dressing room jokes | Cleaning a table with `drop` |

## What I practiced

- Two ways to use an API: a **wrapper library** (`randomuser`) and **raw requests** (`requests.get`)
- Converting JSON to a Pandas DataFrame
- **Flattening nested JSON**: `{"nutritions": {"calories": 96}}` becomes the column `nutritions.calories`
- Filtering a table to look up one row (`df.loc[df["name"] == "Banana"]`)
- Separating *fetching* from *parsing* so the logic can be tested offline

## Project structure

```
api-data-explorer/
├── main.py                 # runs all three demos
├── src/
│   ├── users.py            # RandomUser: squad table
│   ├── fruit.py            # Fruityvice: fetch, flatten, lookups
│   └── jokes.py            # Joke API: fetch and clean
├── tests/test_api_data_explorer.py   # offline tests with sample data
├── output/                 # generated squad.csv (ignored by Git)
├── EXPLAINED.md            # beginner-friendly walkthrough
└── requirements.txt
```

## Run it

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py                   # needs internet
pytest                           # works offline
```

If one API is down, that step prints "Skipped" and the others still run.

## Notes

- RandomUser returns random placeholder people, not real players.
- Public APIs can change or go offline; the tests use sample data so they always pass.

## Tech stack

Python 3.10+, Pandas, Requests, randomuser, Pytest

Based on the IBM "API Examples" lab, rebuilt with reusable functions, error handling and tests.
