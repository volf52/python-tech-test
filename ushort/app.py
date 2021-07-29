from fastapi import FastAPI, HTTPException, Path
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from ushort.db import get_db, get_url_counter
from ushort.schemas import URLShortenRequest
from ushort.shortener import generate_url_id, is_valid_url, validate_url_id

app = FastAPI()


@app.post("/shorten_url")
async def shorten_url(ushort: URLShortenRequest, req: Request):
    url = ushort.url

    if not is_valid_url(url):
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid URL"
        )

    db = get_db()

    url_id = generate_url_id(url)
    db[url_id] = url

    # Update counters
    url_counter = get_url_counter()
    url_counter.update([url])

    return {"shortened_url": f"{req.url.scheme}://{req.url.netloc}/s/{url_id}"}


@app.get("/s/{url_id}", response_class=RedirectResponse)
async def process_short_url(url_id: str = Path(...)):
    msg = validate_url_id(url_id)

    if msg is not None:
        raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail=msg)

    db = get_db()

    long_url = db.get(url_id)

    if long_url is None:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"No matching record found in database for {url_id}",
        )

    return long_url
