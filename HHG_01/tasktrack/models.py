from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import date
from typing import Optional

PRIORITIES = ("low", "medium", "high")
PRIORITY_RANK = {name: i for i, name in enumerate(PRIORITIES)}


@dataclass
class Task:
    id: int
    title: str
    priority: str = "medium"
    due: Optional[str] = None  # ISO date string, e.g. 2026-12-01
    done: bool = False

    def __post_init__(self) -> None:
        self.title = self.title.strip()
        if not self.title:
            raise ValueError("title must not be empty")
        if self.priority not in PRIORITIES:
            raise ValueError(f"priority must be one of {PRIORITIES}")
        if self.due is not None:
            date.fromisoformat(self.due)  # raises ValueError if malformed

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(**data)

    def sort_key(self):
        """Open tasks first, then earliest due date, then highest priority."""
        return (
            self.done,
            self.due or "9999-12-31",
            -PRIORITY_RANK[self.priority],
            self.id,
        )
