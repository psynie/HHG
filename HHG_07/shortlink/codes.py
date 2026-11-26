from __future__ import annotations

import secrets
import string
from urllib.parse import urlparse

ALPHABET = string.digits + string.ascii_lowercase + string.ascii_uppercase  # base62
CODE_LENGTH = 6
MAX_URL_LENGTH = 2048


def new_code(length: int = CODE_LENGTH) -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(length))


def is_valid_code(code: str) -> bool:
    return len(code) == CODE_LENGTH and all(c in ALPHABET for c in code)


def validate_url(url: str) -> str:
    """Return the cleaned URL or raise ValueError."""
    url = url.strip()
    if not url or len(url) > MAX_URL_LENGTH:
        raise ValueError("url is empty or too long")
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("only absolute http(s) URLs are allowed")
    return url
