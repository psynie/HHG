from __future__ import annotations

import csv
from typing import Dict, List, Optional, Tuple

MISSING = {"", "na", "n/a", "null", "none"}


def is_missing(value: str) -> bool:
    return value.strip().lower() in MISSING


def try_float(value: str) -> Optional[float]:
    try:
        return float(value)
    except ValueError:
        return None


def read_columns(path: str) -> Dict[str, List[str]]:
    """Read a CSV into {column name: list of raw string values}."""
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames:
            raise ValueError("CSV file has no header row")
        columns: Dict[str, List[str]] = {name: [] for name in reader.fieldnames}
        for row in reader:
            for name in columns:
                columns[name].append((row.get(name) or "").strip())
    return columns


def infer_column(values: List[str]) -> Tuple[str, List]:
    """Return ('numeric', floats) or ('text', strings), excluding missing values."""
    present = [v for v in values if not is_missing(v)]
    numbers = [try_float(v) for v in present]
    if present and all(n is not None for n in numbers):
        return "numeric", numbers
    return "text", present
