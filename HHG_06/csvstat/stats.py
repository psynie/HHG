from __future__ import annotations

import math
from collections import Counter
from typing import Dict, List


def percentile(sorted_values: List[float], q: float) -> float:
    """Linear-interpolated percentile (q in 0..100) of an already sorted list."""
    if not sorted_values:
        raise ValueError("no values")
    if len(sorted_values) == 1:
        return sorted_values[0]
    rank = (len(sorted_values) - 1) * q / 100
    low = math.floor(rank)
    high = math.ceil(rank)
    frac = rank - low
    return sorted_values[low] + (sorted_values[high] - sorted_values[low]) * frac


def summarize_numeric(values: List[float], missing: int = 0) -> Dict[str, float]:
    data = sorted(values)
    n = len(data)
    mean = sum(data) / n
    # Sample standard deviation (n - 1); undefined for a single value.
    variance = sum((x - mean) ** 2 for x in data) / (n - 1) if n > 1 else float("nan")
    return {
        "count": n,
        "missing": missing,
        "min": data[0],
        "max": data[-1],
        "mean": mean,
        "median": percentile(data, 50),
        "std": math.sqrt(variance) if n > 1 else float("nan"),
        "p25": percentile(data, 25),
        "p75": percentile(data, 75),
    }


def summarize_text(values: List[str], missing: int = 0, top: int = 3) -> dict:
    counts = Counter(values)
    return {
        "count": len(values),
        "missing": missing,
        "unique": len(counts),
        "top": counts.most_common(top),
    }
