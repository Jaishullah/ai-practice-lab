"""Run all HTTP demos: python main.py  (needs an internet connection)"""

from pathlib import Path

import requests

from src.http_client import (
    BASE_URL,
    download_file,
    get_page,
    get_with_params,
    post_form,
)

# Cricket-flavoured payload, reused for GET and POST
PAYLOAD = {"team": "India", "opponent": "Afghanistan", "format": "T20I"}


def main() -> None:
    print("1) GET a web page")
    print(get_page(f"{BASE_URL}/html"), "\n")

    print("2) Download a file")
    saved = download_file(f"{BASE_URL}/image/png", Path("downloads/sample.png"))
    print("Saved to:", saved, f"({saved.stat().st_size} bytes)\n")

    print("3) GET with URL parameters")
    result = get_with_params(PAYLOAD)
    print("URL:", result["url"])
    print("Body:", result["request_body"])
    print("Server received:", result["args"], "\n")

    print("4) POST with a request body")
    result = post_form(PAYLOAD)
    print("URL:", result["url"])
    print("Body:", result["request_body"])
    print("Server received:", result["form"])


if __name__ == "__main__":
    try:
        main()
    except requests.RequestException as error:
        print(f"\nCould not reach the server. Check your internet connection.\nDetails: {error}")
