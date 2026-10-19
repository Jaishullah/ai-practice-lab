# GDP Web Scraping ETL

A small **ETL pipeline** (Extract, Transform, Load) that scrapes the list of the world's largest
economies (IMF figures) from an archived Wikipedia page, cleans it with Pandas and NumPy, and saves
the top 10 to a CSV file.

## Pipeline

```
EXTRACT                     TRANSFORM                         LOAD
web page  ──►  raw table  ──►  top 10 rows, 2 columns  ──►  Million → Billion USD  ──►  CSV file
extract_table()             select_top_economies()          convert_to_billions()      load_to_csv()
```

| Stage | Function | What it does |
|---|---|---|
| Extract | `extract_table()` | Downloads the page with `requests`, finds all HTML tables with `pd.read_html()`, returns table #3 |
| Transform | `select_top_economies()` | Keeps the country and IMF GDP columns and rows 1 to 10 (row 0 is the world total) |
| Transform | `convert_to_billions()` | Million USD ÷ 1000, `np.round(..., 2)`, renames the header to `GDP (Billion USD)` |
| Load | `load_to_csv()` | Saves `output/Largest_economies.csv` |

## What I practiced

- Web scraping tables with `pd.read_html()`
- Selecting columns and rows (`df[[0, 2]]`, `.iloc[1:11]`)
- Cleaning data types and converting units with NumPy
- Writing the ETL stages as separate, testable functions
- Offline unit tests with sample data

## Improvements over the original lab

| Original lab | This project |
|---|---|
| `df.rename(...)` result was never saved, so the header did not change | The renamed table is returned and used |
| `astype(int)` crashes on a bad value | Clear error naming the country with the bad value |
| `to_csv()` writes an extra 0, 1, 2... column | `index=False` |
| Copy of a slice can trigger Pandas warnings | Works on a `.copy()` |

## Run it

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py                   # needs internet
pytest                           # works offline
```

## Notes

- The data comes from an archived snapshot (Sept 2, 2023), so the numbers do not change.
- The scraper expects the IMF table to be table #3 and to have the country first and the IMF value third.
  If the page layout changes, update `TABLE_INDEX` and the column positions in `src/etl.py`.

## Tech stack

Python 3.10+, Pandas, NumPy, Requests, lxml, Pytest

Based on the IBM "GDP data extraction and processing" practice project.
