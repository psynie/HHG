from __future__ import annotations

import argparse
import json
import sys
from typing import Optional, Sequence

from .ledger import Ledger
from .settle import settle


def money(cents: int) -> str:
    sign = "-" if cents < 0 else ""
    return f"{sign}{abs(cents) // 100}.{abs(cents) % 100:02d}"


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="splitlite", description="Settle group expenses")
    parser.add_argument("file", help="JSON file describing the expenses")
    args = parser.parse_args(argv)

    try:
        with open(args.file, encoding="utf-8") as fh:
            ledger = Ledger.from_dict(json.load(fh))
        payments = settle(ledger.balances)
    except (OSError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print("Balances:")
    for person, cents in sorted(ledger.balances.items()):
        label = money(cents) if cents < 0 else "+" + money(cents)
        print(f"  {person:<8}{label:>9}")
    print("\nSettlements:")
    if not payments:
        print("  Everyone is already even.")
    for debtor, creditor, cents in payments:
        print(f"  {debtor} pays {creditor} {money(cents)}")
    return 0
