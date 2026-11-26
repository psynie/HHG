from __future__ import annotations

import math
import re
import string
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from .generator import DATA_DIR, SYMBOLS


@dataclass
class Report:
    entropy_bits: float
    rating: str
    warnings: List[str] = field(default_factory=list)


def _common_passwords() -> set:
    path: Path = DATA_DIR / "common_passwords.txt"
    return {line.strip().lower() for line in path.read_text(encoding="utf-8").splitlines()}


def pool_size(password: str) -> int:
    size = 0
    if re.search(r"[a-z]", password):
        size += 26
    if re.search(r"[A-Z]", password):
        size += 26
    if re.search(r"\d", password):
        size += 10
    if any(c in SYMBOLS or c in string.punctuation or c == " " for c in password):
        size += len(SYMBOLS)
    return size or 1


def has_sequence(password: str, run: int = 4) -> bool:
    """True if the password contains `run` ascending or descending consecutive chars."""
    lowered = password.lower()
    for i in range(len(lowered) - run + 1):
        window = lowered[i:i + run]
        steps = {ord(b) - ord(a) for a, b in zip(window, window[1:])}
        if steps in ({1}, {-1}):
            return True
    return False


def check(password: str) -> Report:
    warnings: List[str] = []
    if len(password) < 12:
        warnings.append("shorter than 12 characters")
    if pool_size(password) <= 36:
        warnings.append("uses few character types")
    if re.search(r"(.)\1{2,}", password):
        warnings.append("contains a character repeated 3+ times")
    if has_sequence(password):
        warnings.append("contains a sequence like abcd or 4321")
    if password.lower() in _common_passwords():
        warnings.append("appears on the common-password list")

    bits = len(password) * math.log2(pool_size(password)) if password else 0.0
    if "appears on the common-password list" in warnings:
        bits = min(bits, 10.0)

    if bits < 40:
        rating = "weak"
    elif bits < 60:
        rating = "fair"
    elif bits < 80:
        rating = "good"
    else:
        rating = "strong"
    return Report(round(bits, 1), rating, warnings)
