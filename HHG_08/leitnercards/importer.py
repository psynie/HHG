from __future__ import annotations

import csv

from .deck import Deck


def import_csv(deck: Deck, path: str) -> tuple:
    """Import 'question,answer' rows. Returns (added, skipped)."""
    added = skipped = 0
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.reader(fh):
            if len(row) < 2 or not row[0].strip():
                skipped += 1
                continue
            if deck.add(row[0].strip(), row[1].strip()):
                added += 1
            else:
                skipped += 1
    deck.save()
    return added, skipped
