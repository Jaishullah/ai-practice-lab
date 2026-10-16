# Code Explained (Beginner Friendly)

## The big idea
An **API** is a way for one program to ask another program for data.
You send a **request**, you get back a **response**, usually as JSON (a list of key-value pairs).
This project follows that same flow with cricket data.

## 1. A dictionary = one team
```python
{"id": 1, "full_name": "India", "abbreviation": "IND"}
```
Think of it as one row on a scorecard. `get_teams()` returns a **list** of these.

## 2. `merge_dicts()`: rows to columns
```python
[{"id": 1}, {"id": 2}]   ->   {"id": [1, 2]}
```
It loops through each team and collects every value under its key.
Pandas needs data shaped like this to build a table.

## 3. `pd.DataFrame(...)`: the table
A DataFrame is an Excel sheet in Python. Handy methods:
- `.head()` shows the first rows
- `.mean()` calculates the average

## 4. `get_team_id()`: filtering
```python
teams_df[teams_df["full_name"] == "India"]
```
Reads as: "keep only rows where full_name is India". Then we take the `id` from that row.

## 5. `RUN_DIFF`: the key number
```python
matches["RUN_DIFF"] = matches["IND_RUNS"] - matches["AFG_RUNS"]
```
Same as subtracting scores. 365 means India scored 365 more runs. A negative number means Afghanistan scored more.

## 6. Home vs Neutral
`split_by_venue()` makes two smaller tables from one big table, then we average each.
Result on the sample data: India's average run difference is larger at home (94.8) than at neutral venues (36.7).

## 7. `fetch_matches_from_api()`: the real REST call
```python
response = requests.get(url, params=..., headers=...)   # request
response.raise_for_status()                              # stop if the server says error
response.json()                                          # response -> Python list
```
`headers` carries your API key, which proves who you are.

## 8. Tests
`pytest` checks that the functions give the right answers, so future changes don't break them.

## Lab-to-project map

| Original lab (NBA) | This project (Cricket) |
|--------------------|------------------------|
| `teams.get_teams()` | `get_teams()` |
| `one_dict()` | `merge_dicts()` |
| find Warriors id | `get_team_id(..., "India")` |
| `LeagueGameFinder` | `get_matches()` / `fetch_matches_from_api()` |
| `PLUS_MINUS` | `RUN_DIFF` |
| Home (`vs.`) / Away (`@`) | `VENUE_TYPE` Home / Neutral |
| Quiz: mean `PTS` | Mean `IND_RUNS` per venue type |
