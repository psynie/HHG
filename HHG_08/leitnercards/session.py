from __future__ import annotations

from datetime import date
from typing import Callable, Optional

from .deck import Deck


def study(deck: Deck, limit: Optional[int] = None, today: Optional[date] = None,
          ask: Callable[[str], str] = input, say: Callable[[str], None] = print) -> tuple:
    """Run a study session. Returns (correct, total)."""
    today = today or date.today()
    cards = deck.due_cards(today, limit)
    if not cards:
        say("Nothing is due. Come back later!")
        return 0, 0

    correct = 0
    for number, card in enumerate(cards, 1):
        say(f"\n[{number}/{len(cards)}] (box {card.box}) {card.question}")
        ask("Press Enter to reveal... ")
        say(f"Answer: {card.answer}")
        while True:
            reply = ask("Did you get it right? [y/n] ").strip().lower()
            if reply in ("y", "n"):
                break
        card.review(reply == "y", today)
        correct += reply == "y"
        deck.save()  # save after every card so quitting midway loses nothing
    say(f"\nSession complete: {correct}/{len(cards)} correct.")
    return correct, len(cards)
