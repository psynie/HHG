from __future__ import annotations

import json
import os
import tempfile
from dataclasses import dataclass, asdict
from datetime import date, timedelta
from pathlib import Path
from typing import List, Optional

INTERVALS = {1: 1, 2: 2, 3: 4, 4: 8, 5: 16}  # box -> days until next review
MAX_BOX = 5


@dataclass
class Card:
    question: str
    answer: str
    box: int = 1
    due: str = ""  # ISO date; empty means due immediately

    def is_due(self, today: date) -> bool:
        return not self.due or date.fromisoformat(self.due) <= today

    def review(self, correct: bool, today: date) -> None:
        self.box = min(self.box + 1, MAX_BOX) if correct else 1
        self.due = (today + timedelta(days=INTERVALS[self.box])).isoformat()


class Deck:
    def __init__(self, path: Optional[os.PathLike] = None):
        self.path = Path(path or Path.home() / ".leitnercards.json")
        self.cards: List[Card] = []
        if self.path.exists():
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            self.cards = [Card(**c) for c in raw]

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=self.path.parent, suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump([asdict(c) for c in self.cards], fh, indent=2)
        os.replace(tmp, self.path)

    def add(self, question: str, answer: str) -> bool:
        """Add a card unless the same question exists. Returns True if added."""
        if any(c.question == question for c in self.cards):
            return False
        self.cards.append(Card(question, answer))
        return True

    def due_cards(self, today: Optional[date] = None, limit: Optional[int] = None) -> List[Card]:
        today = today or date.today()
        due = sorted((c for c in self.cards if c.is_due(today)), key=lambda c: c.box)
        return due[:limit] if limit else due

    def box_counts(self) -> dict:
        counts = {box: 0 for box in INTERVALS}
        for card in self.cards:
            counts[card.box] += 1
        return counts
