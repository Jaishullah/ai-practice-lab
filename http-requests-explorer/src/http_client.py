"""
http_client.py
--------------
Small, reusable helpers that wrap the `requests` library.

Each function does ONE job:
    status_class()     -> explains a status code (200 = Success ...)
    get_page()         -> GET a web page, summarize the response
    download_file()    -> GET a file (image, txt ...) and save it
    get_with_params()  -> GET with a query string  (?name=...&format=...)
    post_form()        -> POST data in the request body
"""

from __future__ import annotations

from pathlib import Path

import requests

BASE_URL = "https://httpbin.org"  # free service that echoes back what you send
TIMEOUT = 10  # seconds; never wait forever for a server


def status_class(code: int) -> str:
    """Translate a status code into plain English."""
    if 200 <= code < 300:
        return "Success"
    if 300 <= code < 400:
        return "Redirect"
    if 400 <= code < 500:
        return "Client error (your request has a problem)"
    if 500 <= code < 600:
        return "Server error (the server has a problem)"
    return "Informational"


def get_page(url: str) -> dict:
    """GET a page and return the key facts about the response."""
    response = requests.get(url, timeout=TIMEOUT)
    return {
        "status_code": response.status_code,
        "meaning": status_class(response.status_code),
        "content_type": response.headers.get("Content-Type"),
        "encoding": response.encoding,
        "preview": response.text[:100],
    }


def download_file(url: str, destination: Path | str) -> Path:
    """GET a file and save its raw bytes to `destination`."""
    response = requests.get(url, timeout=TIMEOUT)
    response.raise_for_status()  # stop here if the server returned 4xx / 5xx
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(response.content)  # .content = raw bytes
    return destination


def get_with_params(params: dict) -> dict:
    """GET with a query string. The data travels inside the URL."""
    response = requests.get(f"{BASE_URL}/get", params=params, timeout=TIMEOUT)
    response.raise_for_status()
    return {
        "url": response.url,
        "request_body": response.request.body,  # None for GET
        "args": response.json()["args"],
    }


def post_form(data: dict) -> dict:
    """POST form data. The data travels inside the request body."""
    response = requests.post(f"{BASE_URL}/post", data=data, timeout=TIMEOUT)
    response.raise_for_status()
    return {
        "url": response.url,  # no ?name=... here
        "request_body": response.request.body,
        "form": response.json()["form"],
    }
