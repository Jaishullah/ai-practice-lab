# HTTP Requests Explorer

A small Python lab that shows how a program talks to a web server using HTTP:
**GET**, **GET with parameters**, **POST**, and **file downloads**.

It uses [httpbin.org](https://httpbin.org), a free service that echoes back whatever you send,
so you can see exactly what travels in the URL, headers and body.

## What I practiced

| Concept | Function | Key idea |
|---|---|---|
| Status codes | `status_class()` | 2xx success, 4xx your mistake, 5xx server's mistake |
| GET a page | `get_page()` | `status_code`, `headers`, `.text` |
| Download a file | `download_file()` | `.content` (bytes) saved with `write_bytes` |
| URL parameters | `get_with_params()` | data goes in the URL: `?team=India` |
| POST | `post_form()` | data goes in the request body, URL stays clean |
| Error handling | `raise_for_status()`, `timeout` | fail loudly instead of silently |

## GET vs POST

| | GET | POST |
|---|---|---|
| Purpose | ask for data | send data |
| Data location | URL (`?team=India&...`) | request body |
| Request body | `None` | the form data |

## Project structure

```
http-requests-explorer/
├── main.py                  # runs every demo
├── src/http_client.py       # the reusable request helpers
├── tests/test_http_client.py  # offline tests (fake responses, no internet needed)
├── downloads/               # downloaded files land here (ignored by Git)
├── EXPLAINED.md             # beginner-friendly walkthrough
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

## Example output (shape)

```
3) GET with URL parameters
URL: https://httpbin.org/get?team=India&opponent=Afghanistan&format=T20I
Body: None

4) POST with a request body
URL: https://httpbin.org/post
Body: team=India&opponent=Afghanistan&format=T20I
```

## Tech stack

Python 3.10+, Requests, Pytest

Based on the IBM "HTTP and Requests" lab, rebuilt with reusable functions, timeouts, error handling and tests.
