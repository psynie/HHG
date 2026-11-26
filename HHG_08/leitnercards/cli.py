from __future__ import annotations

import argparse
import sys
from typing import Optional, Sequence

from .deck import Deck, INTERVALS
from .importer import import_csv
from .session import study


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="leitnercards")
    parser.add_argument("--file", help="path to the progress file")
    sub = parser.add_subparsers(dest="command", required=True)

    imp = sub.add_parser("import", help="import cards from a CSV file")
    imp.add_argument("csv")
    st = sub.add_parser("study", help="review cards that are due")
    st.add_argument("--limit", type=int)
    sub.add_parser("stats", help="show cards per box")

    args = parser.parse_args(argv)
    deck = Deck(args.file)
    try:
        if args.command == "import":
            added, skipped = import_csv(deck, args.csv)
            print(f"Imported {added} card(s), skipped {skipped}.")
        elif args.command == "study":
            study(deck, args.limit)
        else:
            print(f"Total cards: {len(deck.cards)}   Due now: {len(deck.due_cards())}")
            for box, count in deck.box_counts().items():
                print(f"  Box {box} (every {INTERVALS[box]:>2}d): {count}")
    except (OSError, EOFError, KeyboardInterrupt) as exc:
        print(f"\nstopped: {exc or 'interrupted'}", file=sys.stderr)
        return 1
    return 0
