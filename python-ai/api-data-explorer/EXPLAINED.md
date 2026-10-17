# Code Explained (Beginner Friendly)

## The story
A team manager needs three things: **a squad list**, **a diet plan**, and **a few jokes**.
Each comes from a different API, and each file handles one of them.

Every file follows the same pattern: **fetch → convert to table → use it.**

## `src/users.py` - the squad
```python
users = RandomUser.generate_users(10)   # API call: 10 random people
return build_squad_df(users)            # turn them into a table
```
- `generate_users()` is the request. The library hides the HTTP details for you.
- `build_squad_df()` loops through the users and picks out name, gender, city, etc.
  Each `user.get_full_name()` is one of the "Get Methods" from the lab.
- Result: a table with one row per player.

## `src/fruit.py` - the diet plan
```python
response = requests.get(FRUIT_URL, timeout=10)   # request / response
response.raise_for_status()                      # stop if the server errored
return response.json()                           # JSON -> Python list
```
- The fruit data is **nested**: `nutritions` is a dictionary inside each fruit.
- `pd.json_normalize()` **flattens** it into columns like `nutritions.calories`.
- `get_calories(df, "Banana")` filters the table to one row, then reads that column.
- `get_family_and_genus(df, "Cherry")` does the same for two other columns.

## `src/jokes.py` - the dressing room
Fetch the list, make a table, then `drop(columns=["type", "id"])` removes what we don't need.

## `main.py` - the producer
It calls the three demos in order. `run_section()` wraps each one in `try/except`,
so if one API is down, the others still run.

## How the files connect
```
main.py
 ├─ demo_squad()  ─► users.get_squad()  ─► build_squad_df()  ─► squad.csv
 ├─ demo_fruit()  ─► fruit.fetch_fruit_data() ─► fruits_to_df() ─► get_calories()
 └─ demo_jokes()  ─► jokes.fetch_jokes() ─► jokes_to_df()
```

## Why "fetch" and "convert" are separate functions
Fetching needs the internet, so it can fail. Converting is pure logic.
Splitting them means the tests can feed in sample data and check the logic without any API.
