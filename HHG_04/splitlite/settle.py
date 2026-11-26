from __future__ import annotations

from typing import Dict, List, Tuple

Payment = Tuple[str, str, int]  # (from, to, cents)


def settle(balances: Dict[str, int]) -> List[Payment]:
    """Return payments that bring every balance to zero.

    Positive balance means the person is owed money. Balances must sum to zero.
    """
    if sum(balances.values()) != 0:
        raise ValueError("balances do not sum to zero")

    creditors = sorted(((v, p) for p, v in balances.items() if v > 0), reverse=True)
    debtors = sorted(((-v, p) for p, v in balances.items() if v < 0), reverse=True)
    payments: List[Payment] = []

    while creditors and debtors:
        credit, creditor = creditors.pop(0)
        debt, debtor = debtors.pop(0)
        amount = min(credit, debt)
        payments.append((debtor, creditor, amount))
        if credit > amount:
            creditors.append((credit - amount, creditor))
            creditors.sort(reverse=True)
        if debt > amount:
            debtors.append((debt - amount, debtor))
            debtors.sort(reverse=True)
    return payments
