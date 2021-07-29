import pytest
from fastapi.testclient import TestClient
from requests import Response

from ushort.app import app
from ushort.db import COUNTER_KEY, URL_TABLE_NAME, get_db, get_url_freq
from ushort.shortener import validate_url_id

client = TestClient(app)


@pytest.fixture(scope="function")
def setup():
    get_db()[URL_TABLE_NAME] = {}
    get_db()[COUNTER_KEY] = 0
    get_url_freq().clear()


@pytest.mark.parametrize(
    "url",
    [
        "https://fastapi.tiangolo.com/features/",
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://exercism.io/tracks/python",
        "https://doc.rust-lang.org/book/ch03-00-common-programming-concepts.html",
        "https://doc.rust-lang.org/stable/rust-by-example/index.html",
    ],
)
def test_shorten_url_route(url: str, setup):
    resp: Response = client.post("/shorten_url", json={"url": url})

    assert resp.status_code == 201

    resp_data: dict = resp.json()

    assert resp_data.keys() == {"shortened_url"}

    shortened_url: str = resp_data["shortened_url"]

    assert shortened_url.startswith(f"{client.base_url}/s/")

    assert validate_url_id(shortened_url.rsplit("/", maxsplit=1)[-1]) is None


@pytest.mark.parametrize(
    "url",
    [
        "https://fastapi.tiangolo.com/features/",
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://exercism.io/tracks/python",
        "https://doc.rust-lang.org/book/ch03-00-common-programming-concepts.html",
        "https://doc.rust-lang.org/stable/rust-by-example/index.html",
    ],
)
def test_redirect_to_long_url(url: str, setup):
    resp = client.post("/shorten_url", json={"url": url})

    assert resp.status_code == 201

    shortened = resp.json()["shortened_url"][len(client.base_url) :]

    resp2 = client.get(shortened, allow_redirects=False)

    assert resp2.status_code == 307

    assert resp2.headers.get("location") == url


def test_url_counter(setup):
    assert client.get("/shortened_urls_count").json() == 0

    urls = [
        "https://fastapi.tiangolo.com/features/",
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://exercism.io/tracks/python",
        "https://doc.rust-lang.org/book/ch03-00-common-programming-concepts.html",
        "https://doc.rust-lang.org/stable/rust-by-example/index.html",
    ]
    for url in urls:
        resp = client.post("/shorten_url", json={"url": url})
        assert resp.status_code == 201

    assert client.get("/shortened_urls_count").json() == len(urls)


def test_popular_urls(setup):
    assert client.get("/shortened_urls_count").json() == 0

    url1 = "https://fastapi.tiangolo.com/features/"
    url2 = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    resp = client.post("/shorten_url", json={"url": url1})
    assert resp.status_code == 201

    def assert_is_most_pop(urls: list):
        expected = f"<p><strong>Most popular urls: </strong>{', '.join(f'<a href={x}>{x}</a>' for x in urls)}</p>"
        actual = client.get("/").content.decode("utf-8")

        assert expected == actual

    assert_is_most_pop([url1])

    resp = client.post("/shorten_url", json={"url": url2})
    assert resp.status_code == 201
    resp = client.post("/shorten_url", json={"url": url2})
    assert resp.status_code == 201

    assert_is_most_pop([url2, url1])

    resp = client.post("/shorten_url", json={"url": url1})
    assert resp.status_code == 201
    resp = client.post("/shorten_url", json={"url": url1})
    assert resp.status_code == 201

    assert_is_most_pop([url1, url2])
