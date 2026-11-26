import tempfile
import unittest
from datetime import date
from pathlib import Path

from leitnercards.deck import Card, Deck
from leitnercards.importer import import_csv

TODAY = date(2026, 11, 26)


class CardTests(unittest.TestCase):
    def test_correct_moves_up_and_schedules(self):
        card = Card("q", "a")
        card.review(True, TODAY)
        self.assertEqual(card.box, 2)
        self.assertEqual(card.due, "2026-11-28")  # 2 days for box 2

    def test_wrong_resets_to_box_one(self):
        card = Card("q", "a", box=4)
        card.review(False, TODAY)
        self.assertEqual(card.box, 1)
        self.assertEqual(card.due, "2026-11-27")

    def test_box_is_capped(self):
        card = Card("q", "a", box=5)
        card.review(True, TODAY)
        self.assertEqual(card.box, 5)

    def test_due_logic(self):
        self.assertTrue(Card("q", "a").is_due(TODAY))
        self.assertFalse(Card("q", "a", due="2026-12-01").is_due(TODAY))
        self.assertTrue(Card("q", "a", due="2026-11-26").is_due(TODAY))


class DeckTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = Path(self.dir.name) / "deck.json"

    def tearDown(self):
        self.dir.cleanup()

    def test_duplicates_ignored(self):
        deck = Deck(self.path)
        self.assertTrue(deck.add("q", "a"))
        self.assertFalse(deck.add("q", "b"))

    def test_persistence(self):
        deck = Deck(self.path)
        deck.add("q", "a")
        deck.save()
        self.assertEqual(len(Deck(self.path).cards), 1)

    def test_import_csv(self):
        csv_path = Path(self.dir.name) / "cards.csv"
        csv_path.write_text('one,1\ntwo,2\none,dup\n,blank\n', encoding="utf-8")
        added, skipped = import_csv(Deck(self.path), str(csv_path))
        self.assertEqual((added, skipped), (2, 2))


if __name__ == "__main__":
    unittest.main()
