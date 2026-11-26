from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

LINE_RE = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] '
    r'"(?P<method>[A-Z]+) (?P<path>\S+)[^"]*" '
    r'(?P<status>\d{3}) (?P<bytes>\d+|-)'
)
TIME_FORMAT = "%d/%b/%Y:%H:%M:%S %z"


@dataclass(frozen=True)
class Entry:
    ip: str
    time: datetime
    method: str
    path: str
    status: int
    size: int


def parse_line(line: str) -> Optional[Entry]:
    """Parse one log line, returning None if it does not match the format."""
    match = LINE_RE.match(line.strip())
    if not match:
        return None
    try:
        when = datetime.strptime(match["time"], TIME_FORMAT)
    except ValueError:
        return None
    size = 0 if match["bytes"] == "-" else int(match["bytes"])
    return Entry(
        ip=match["ip"],
        time=when,
        method=match["method"],
        path=match["path"].split("?", 1)[0],
        status=int(match["status"]),
        size=size,
    )
