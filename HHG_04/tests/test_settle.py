import json
import unittest
from pathlib import Path

from splitlite.ledger import Ledger
from splitlite.settle import settle

EXAMPLE = Path(__file__).resolve().parent.parent / "examples" / "trip.json"


class SettleTests(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(settle({"a": 500, "b": -500}), [("b", "a", 500)])

    def test_payments_clear_all_balances(self):
        balances = {"a": 700, "b": -200, "c": -300, "d": -200}
        after = dict(balances)
        for debtor, creditor, cents in settle(balances):
            after[debtor] += cents
            after[creditor] -= cents
        self.assertTrue(all(v == 0 for v in after.values()))

    def test_at_most_n_minus_one_payments(self):
        balances = {"a": 700, "b": -200, "c": -300, "d": -200}
        self.assertLessEqual(len(settle(balances)), 3)

    def test_unbalanced_input_rejected(self):
        with self.assertRaises(ValueError):
            settle({"a": 100})

    def test_example_file(self):
        ledger = Ledger.from_dict(json.loads(EXAMPLE.read_text()))
        self.assertEqual(
            sorted(settle(ledger.balances)),
            [("Ben", "Asha", 2500), ("Chitra", "Asha", 5500)],
        )


if __name__ == "__main__":
    unittest.main()
