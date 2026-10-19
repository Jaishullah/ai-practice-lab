"""Run the ETL pipeline: python main.py  (needs internet)"""

import requests

from src.etl import convert_to_billions, extract_table, load_to_csv, select_top_economies


def main() -> None:
    print("EXTRACT: downloading the web page ...")
    raw = extract_table()
    print(f"  found a table with {raw.shape[0]} rows and {raw.shape[1]} columns")

    print("\nTRANSFORM 1: keep country + GDP, top 10 rows")
    top = select_top_economies(raw)
    print(top)

    print("\nTRANSFORM 2: million USD -> billion USD")
    final = convert_to_billions(top)
    print(final)

    print("\nLOAD: saving to CSV")
    print("  saved:", load_to_csv(final))


if __name__ == "__main__":
    try:
        main()
    except requests.RequestException as error:
        print(f"Could not download the page. Check your internet connection.\nDetails: {error}")
