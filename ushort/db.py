from collections import Counter
from functools import lru_cache
from typing import Dict


@lru_cache(maxsize=1)
def get_db() -> Dict[str, str]:
    return {}


@lru_cache(maxsize=1)
def get_url_counter() -> Counter:
    return Counter()
