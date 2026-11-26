from __future__ import annotations

from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Iterable, List


def to_cents(amount) -> int:
    """Convert a number or numeric string such as '12.34' to integer cents."""
    value = Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return int(value * 100)


def split_evenly(total_cents: int, people: List[str]) -> Dict[str, int]:
    """Split cents among people; the first `remainder` people get one extra cent."""
    if not people:
        raise ValueError("an expense needs at least one person to share it")
    base, remainder = divmod(total_cents, len(people))
    return {p: base + (1 if i < remainder else 0) for i, p in enumerate(people)}


class Ledger:
    def __init__(self) -> None:
        self._balances: Dict[str, int] = defaultdict(int)

    def add_expense(self, payer: str, amount, shared_by: Iterable[str]) -> None:
        cents = to_cents(amount)
        if cents <= 0:
            raise ValueError("amount must be positive")
        shares = split_evenly(cents, list(shared_by))
        self._balances[payer] += cents
        for person, owed in shares.items():
            self._balances[person] -= owed

    @property
    def balances(self) -> Dict[str, int]:
        return dict(self._balances)

    @classmethod
    def from_dict(cls, data: dict) -> "Ledger":
        ledger = cls()
        for exp in data["expenses"]:
            ledger.add_expense(exp["payer"], exp["amount"], exp["shared_by"])
        return ledger
