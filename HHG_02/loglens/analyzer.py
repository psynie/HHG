from __future__ import annotations

from collections import Counter
from typing import Iterable

from .parser import parse_line


def analyze(lines: Iterable[str], top: int = 10) -> dict:
    ips: Counter = Counter()
    paths: Counter = Counter()
    classes: Counter = Counter()
    hours: Counter = Counter()
    total = 0
    total_bytes = 0
    bad = 0

    for line in lines:
        if not line.strip():
            continue
        entry = parse_line(line)
        if entry is None:
            bad += 1
            continue
        total += 1
        total_bytes += entry.size
        ips[entry.ip] += 1
        paths[entry.path] += 1
        classes[f"{entry.status // 100}xx"] += 1
        hours[entry.time.strftime("%Y-%m-%d %H:00")] += 1

    return {
        "total_requests": total,
        "total_bytes": total_bytes,
        "unparsed_lines": bad,
        "status_classes": dict(sorted(classes.items())),
        "top_ips": ips.most_common(top),
        "top_paths": paths.most_common(top),
        "requests_per_hour": dict(sorted(hours.items())),
    }
