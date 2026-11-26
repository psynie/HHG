from __future__ import annotations

import secrets
import string
from pathlib import Path
from typing import List, Optional

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.?"


def build_classes(lower=True, upper=True, digits=True, symbols=True) -> List[str]:
    classes = []
    if lower:
        classes.append(string.ascii_lowercase)
    if upper:
        classes.append(string.ascii_uppercase)
    if digits:
        classes.append(string.digits)
    if symbols:
        classes.append(SYMBOLS)
    if not classes:
        raise ValueError("at least one character class must be enabled")
    return classes


def generate_password(length: int = 16, **class_options) -> str:
    classes = build_classes(**class_options)
    if length < len(classes):
        raise ValueError(f"length must be at least {len(classes)} for these options")
    pool = "".join(classes)
    # One guaranteed character from each class, the rest from the full pool.
    chars = [secrets.choice(c) for c in classes]
    chars += [secrets.choice(pool) for _ in range(length - len(chars))]
    # Fisher-Yates shuffle driven by secrets, so positions are unpredictable.
    for i in range(len(chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        chars[i], chars[j] = chars[j], chars[i]
    return "".join(chars)


def load_words(path: Optional[Path] = None) -> List[str]:
    path = path or DATA_DIR / "words.txt"
    return [w.strip() for w in path.read_text(encoding="utf-8").splitlines() if w.strip()]


def generate_passphrase(words: int = 4, separator: str = "-",
                        wordlist: Optional[List[str]] = None) -> str:
    if words < 1:
        raise ValueError("need at least one word")
    wordlist = wordlist or load_words()
    return separator.join(secrets.choice(wordlist) for _ in range(words))
