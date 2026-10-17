# Code Explained (Beginner Friendly)

## The story
Your program is a **customer**, the web is a **restaurant**.
You send an **order** (request), and the kitchen sends back a **dish** (response).

## `status_class(code)` - reading the receipt
Every response has a number. This function translates it:
`200` Success, `404` you asked for something that doesn't exist, `500` the server broke.

## `get_page(url)` - ask for a web page
```python
response = requests.get(url, timeout=10)
```
`response` holds everything: `.status_code`, `.headers`, `.text`.
The function returns a short summary instead of dumping all of it.

## `download_file(url, destination)` - save a file
```python
response.raise_for_status()                 # 1. stop if the server said error
destination.write_bytes(response.content)   # 2. save the raw bytes
```
Pages are text (`.text`). Images and files are bytes (`.content`).

## `get_with_params(params)` - a filtered question
```python
requests.get(url, params={"team": "India"})
# becomes https://httpbin.org/get?team=India
```
The dictionary turns into a **query string**. Data is visible in the URL and the body is `None`.

## `post_form(data)` - send data privately
```python
requests.post(url, data={"team": "India"})
```
The data goes inside the **body**, so the URL stays clean.

## How the files connect
```
main.py (producer)
  ├─ get_page()        -> uses status_class()
  ├─ download_file()   -> saves into downloads/
  ├─ get_with_params() -> GET, data in the URL
  └─ post_form()       -> POST, data in the body
```

## Why the tests don't need internet
Tests replace `requests.get` with a **fake** that returns prepared answers (`monkeypatch`).
Good tests are fast, repeatable and never depend on someone else's server.
