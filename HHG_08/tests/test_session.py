import tempfile
import unittest
from datetime import date
from pathlib import Path

from leitnercards.deck import Deck
from leitnercards.session import study

TODAY = date(2026, 11, 26)


class SessionTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.deck = Deck(Path(self.dir.name) / "deck.json")
        self.deck.add("q1", "a1")
        self.deck.add("q2", "a2")
        self.output = []

    def tearDown(self):
        self.dir.cleanup()

    def run_session(self, replies):
        feed = iter(replies)
        return study(self.deck, today=TODAY, ask=lambda _prompt: next(feed),
                     say=self.output.append)

    def test_scoring_and_scheduling(self):
        # card 1: reveal, y   card 2: reveal, n
        correct, total = self.run_session(["", "y", "", "n"])
        self.assertEqual((correct, total), (1, 2))
        boxes = sorted(c.box for c in self.deck.cards)
        self.assertEqual(boxes, [1, 2])

    def test_invalid_reply_is_reasked(self):
        correct, total = self.run_session(["", "maybe", "y", "", "y"])
        self.assertEqual((correct, total), (2, 2))

    def test_nothing_due_after_session(self):
        self.run_session(["", "y", "", "y"])
        self.assertEqual(self.run_session([]), (0, 0))

    def test_progress_is_saved(self):
        self.run_session(["", "y", "", "y"])
        reloaded = Deck(self.deck.path)
        self.assertTrue(all(c.box == 2 for c in reloaded.cards))


if __name__ == "__main__":
    unittest.main()
