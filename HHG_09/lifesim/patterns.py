from __future__ import annotations

from typing import Set, Tuple

LIVE_CHARS = {"O", "#", "*"}
DEAD_CHARS = {".", " "}


def parse_pattern(text: str) -> Set[Tuple[int, int]]:
    """Parse a plain-text pattern into a set of (x, y) live cells."""
    cells = set()
    y = 0
    for raw in text.splitlines():
        line = raw.rstrip()
        if line.startswith("!"):
            continue  # comment
        for x, ch in enumerate(line):
            if ch in LIVE_CHARS:
                cells.add((x, y))
            elif ch not in DEAD_CHARS:
                raise ValueError(f"unexpected character {ch!r} at line {y + 1}, column {x + 1}")
        y += 1
    return cells


def load_pattern(path: str) -> Set[Tuple[int, int]]:
    with open(path, encoding="utf-8") as fh:
        cells = parse_pattern(fh.read())
    if not cells:
        raise ValueError("pattern contains no live cells")
    return cells
