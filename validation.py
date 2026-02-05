from typing import Optional
import re


def read_url_from_request(request) -> Optional[str]:
    pass


def is_valid_url(url: str) -> bool:
    url_pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
    return re.match(url_pattern, url) is not None


def normalize_url(url: str) -> str:
    pass