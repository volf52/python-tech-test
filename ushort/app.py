from fastapi import FastAPI, HTTPException, Path
from fastapi.requests import Request
from fastapi.responses import Response, HTMLResponse, RedirectResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from ushort.db import get_url_count, get_url_freq, get_url_table, update_url_count
from ushort.schemas import URLShortenRequest
from ushort.shortener import generate_url_id, is_valid_url, validate_url_id

app = FastAPI()


@app.post("/shorten_url")
async def shorten_url(ushort: URLShortenRequest, req: Request, resp: Response):
    url = ushort.url

    if not is_valid_url(url):
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid URL"
        )

    url_table = get_url_table()

    url_id = generate_url_id(url)
    url_table[url_id] = url

    # Update counters
    update_url_count()

    url_counter = get_url_freq()
    url_counter.update([url])

    resp.status_code = 201

    return {"shortened_url": f"{req.url.scheme}://{req.url.netloc}/s/{url_id}"}


@app.get("/s/{url_id}", response_class=RedirectResponse)
async def process_short_url(url_id: str = Path(...)):
    msg = validate_url_id(url_id)

    if msg is not None:
        raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail=msg)

    url_table = get_url_table()

    long_url = url_table.get(url_id)

    if long_url is None:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"No matching record found in database for {url_id}",
        )

    return long_url


@app.get("/shortened_urls_count")
async def url_count():
    return get_url_count()


@app.get("/", response_class=HTMLResponse)
async def show_most_popular():
    cntr = get_url_freq()

    most_popular_10 = cntr.most_common(n=10)
    mp10_string = ", ".join(f"<a href={x[0]}>{x[0]}</a>" for x in most_popular_10)

    return f"<p><strong>Most popular urls: </strong>{mp10_string}</p>"
