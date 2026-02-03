from typing import Optional
import urllib.parse


def read_url_from_request(request) -> Optional[str]:
    pass


def is_valid_url(url: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    return parsed.scheme in ['http', 'https'] and parsed.netloc != ''


def normalize_url(url: str) -> str:
    pass