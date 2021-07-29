from collections import Counter
from functools import lru_cache

URL_TABLE_NAME = "url_mapping"
COUNTER_KEY = "count"


@lru_cache(maxsize=1)
def get_db() -> dict:
    return {COUNTER_KEY: 0, URL_TABLE_NAME: {}}


def get_url_table():
    return get_db()[URL_TABLE_NAME]


@lru_cache(maxsize=1)
def get_url_freq() -> Counter:
    return Counter()


def update_url_count():
    db = get_db()
    db[COUNTER_KEY] += 1


def get_url_count():
    return get_db()[COUNTER_KEY]
