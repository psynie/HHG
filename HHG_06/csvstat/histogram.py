from __future__ import annotations

from typing import List


def histogram(values: List[float], bins: int = 5, width: int = 30) -> str:
    if not values:
        return "(no data)"
    if bins < 1:
        raise ValueError("bins must be at least 1")
    lo, hi = min(values), max(values)
    span = (hi - lo) or 1.0
    counts = [0] * bins
    for v in values:
        index = min(int((v - lo) / span * bins), bins - 1)
        counts[index] += 1
    peak = max(counts)
    lines = []
    for i, count in enumerate(counts):
        start = lo + span * i / bins
        end = lo + span * (i + 1) / bins
        bar = "#" * round(count / peak * width) if peak else ""
        lines.append(f"{start:8.2f} - {end:8.2f} | {bar} {count}")
    return "\n".join(lines)
