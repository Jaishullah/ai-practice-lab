# Code Explained (Beginner Friendly)

## The story
A company wants to expand abroad. Your job: **find the 10 biggest economies**, clean the numbers,
and save them in a file. That job is called **ETL**, and you do it in three steps.

```
Extract (get it)  →  Transform (fix it)  →  Load (save it)
```

## 1. Extract: `extract_table()`
```python
response = requests.get(url, headers=HEADERS, timeout=30)   # ask the website
tables = pd.read_html(StringIO(response.text))              # find every <table> on the page
return tables[3]                                            # take the 4th one
```
- A web page can hold many tables. `read_html` returns them as a **list of DataFrames**.
- Lists start counting at **0**, so `[3]` is the **4th** table. The lab says "third" because the
  screenshot counts differently, but the code index is 3.
- `headers` pretends to be a normal browser, because some sites refuse unknown programs.

## 2. Transform, step 1: `select_top_economies()`
The raw table has many columns and messy two-level headers.
```python
df.columns = range(df.shape[1])   # rename columns to 0, 1, 2, 3 ... (easy to pick)
df = df[[0, 2]]                   # keep column 0 (country) and column 2 (IMF GDP)
df = df.iloc[1:11, :]             # keep rows 1 to 10
df.columns = ["Country", "GDP (Million USD)"]
```
- Why start at row **1**? Row 0 is the **World total**, not a country.
- `iloc[1:11]` means "from row 1 up to, but not including, row 11" = 10 rows.

## 3. Transform, step 2: `convert_to_billions()`
```python
numbers = pd.to_numeric(cleaned, errors="coerce")   # text -> numbers
df["GDP (Million USD)"] = np.round(numbers / 1000, 2)
return df.rename(columns={"GDP (Million USD)": "GDP (Billion USD)"})
```
- 1 billion = 1,000 million, so **divide by 1000**.
- `np.round(x, 2)` keeps 2 decimals: `26949.6428` becomes `26949.64`.
- `rename()` does **not** change the table by itself. It returns a new one, so we must `return` it.
  (The original lab forgot this, so its header never changed.)

## 4. Load: `load_to_csv()`
```python
df.to_csv(path, index=False)
```
`index=False` stops Pandas from adding the 0, 1, 2... row numbers as an extra column.

## 5. `run_pipeline()` and `main.py`
`run_pipeline()` calls the four functions in order. Each one's **output** becomes the next one's **input**:
```
extract_table() → raw → select_top_economies() → top → convert_to_billions() → final → load_to_csv()
```
`main.py` does the same steps but prints the table after each one, so you can **watch it change**.

## Lab to project map

| Lab step | Project function |
|---|---|
| Exercise 1: read table 3, keep columns 0 and 2, rows 1 to 10 | `extract_table()` + `select_top_economies()` |
| Exercise 2: Million to Billion, round, rename | `convert_to_billions()` |
| Exercise 3: save CSV | `load_to_csv()` |

## Why the tests work offline
The transform functions only need a table, not the internet. Tests give them small **sample tables**
(numbers made up), so they run fast and never depend on a website.
