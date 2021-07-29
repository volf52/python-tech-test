from secrets import choice
from string import ascii_letters, digits
from typing import Optional

import validators

CHOICES = ascii_letters + digits


def generate_url_id(url: str, *, choices=CHOICES) -> str:
    return "".join(choice(choices) for _ in range(7))


def validate_url_id(url_id: str) -> Optional[str]:
    if len(url_id) != 7:
        return "Invalid length for the URL ID"

    if not all(x in CHOICES for x in url_id):
        return "URL ID has some invalid characters"


def is_valid_url(url: str) -> bool:
    return not isinstance(validators.url(url), validators.ValidationFailure)
