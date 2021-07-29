from pydantic import BaseModel


class URLShortenRequest(BaseModel):
    url: str
