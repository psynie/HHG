import unittest

from splitlite.ledger import Ledger, split_evenly, to_cents


class LedgerTests(unittest.TestCase):
    def test_to_cents(self):
        self.assertEqual(to_cents("12.34"), 1234)
        self.assertEqual(to_cents(5), 500)
        self.assertEqual(to_cents("0.005"), 1)  # rounds half up

    def test_split_keeps_total(self):
        shares = split_evenly(100, ["a", "b", "c"])
        self.assertEqual(sum(shares.values()), 100)
        self.assertEqual(shares, {"a": 34, "b": 33, "c": 33})

    def test_balances_sum_to_zero(self):
        ledger = Ledger()
        ledger.add_expense("a", "10.00", ["a", "b", "c"])
        ledger.add_expense("b", "7.77", ["a", "b"])
        self.assertEqual(sum(ledger.balances.values()), 0)

    def test_rejects_bad_input(self):
        ledger = Ledger()
        with self.assertRaises(ValueError):
            ledger.add_expense("a", "0", ["a"])
        with self.assertRaises(ValueError):
            ledger.add_expense("a", "5", [])


if __name__ == "__main__":
    unittest.main()
