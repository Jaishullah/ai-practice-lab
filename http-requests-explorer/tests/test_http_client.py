"""Tests use a fake `requests` so they run offline and never hit the network."""

import pytest

from src import http_client


class FakeResponse:
    def __init__(self, status=200, headers=None, text="", content=b"", json_data=None, url=""):
        self.status_code = status
        self.headers = headers or {}
        self.encoding = "utf-8"
        self.text = text
        self.content = content
        self._json = json_data
        self.url = url
        self.request = type("Req", (), {"body": None})()

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code >= 400:
            raise http_client.requests.HTTPError(f"{self.status_code} error")


@pytest.mark.parametrize(
    "code, word",
    [(200, "Success"), (301, "Redirect"), (404, "Client"), (500, "Server")],
)
def test_status_class(code, word):
    assert word in http_client.status_class(code)


def test_get_page(monkeypatch):
    fake = FakeResponse(headers={"Content-Type": "text/html"}, text="<html>" + "x" * 200)
    monkeypatch.setattr(http_client.requests, "get", lambda *a, **k: fake)
    info = http_client.get_page("https://example.com")
    assert info["status_code"] == 200
    assert info["content_type"] == "text/html"
    assert len(info["preview"]) == 100


def test_download_file_saves_bytes(monkeypatch, tmp_path):
    monkeypatch.setattr(http_client.requests, "get", lambda *a, **k: FakeResponse(content=b"\x89PNG"))
    saved = http_client.download_file("https://x/y.png", tmp_path / "out" / "y.png")
    assert saved.read_bytes() == b"\x89PNG"


def test_download_file_raises_on_404(monkeypatch, tmp_path):
    monkeypatch.setattr(http_client.requests, "get", lambda *a, **k: FakeResponse(status=404))
    with pytest.raises(http_client.requests.HTTPError):
        http_client.download_file("https://x/missing", tmp_path / "f.bin")


def test_get_with_params_passes_params(monkeypatch):
    seen = {}

    def fake_get(url, params=None, timeout=None):
        seen["params"] = params
        return FakeResponse(json_data={"args": params}, url=url + "?team=India")

    monkeypatch.setattr(http_client.requests, "get", fake_get)
    result = http_client.get_with_params({"team": "India"})
    assert seen["params"] == {"team": "India"}
    assert result["request_body"] is None


def test_post_form_sends_data_in_body(monkeypatch):
    seen = {}

    def fake_post(url, data=None, timeout=None):
        seen["data"] = data
        return FakeResponse(json_data={"form": data}, url=url)

    monkeypatch.setattr(http_client.requests, "post", fake_post)
    result = http_client.post_form({"team": "India"})
    assert seen["data"] == {"team": "India"}
    assert "?" not in result["url"]
