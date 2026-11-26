import unittest
from pathlib import Path

from lifesim.patterns import load_pattern, parse_pattern

PATTERNS = Path(__file__).resolve().parent.parent / "patterns"


class PatternTests(unittest.TestCase):
    def test_parse_simple(self):
        self.assertEqual(parse_pattern("O.\n.O"), {(0, 0), (1, 1)})

    def test_comments_do_not_shift_rows(self):
        self.assertEqual(parse_pattern("! note\nO"), {(0, 0)})

    def test_alternative_live_chars(self):
        self.assertEqual(parse_pattern("#*"), {(0, 0), (1, 0)})

    def test_bad_character(self):
        with self.assertRaises(ValueError):
            parse_pattern("O?O")

    def test_bundled_patterns_load(self):
        self.assertEqual(len(load_pattern(str(PATTERNS / "glider.txt"))), 5)
        self.assertEqual(len(load_pattern(str(PATTERNS / "block.txt"))), 4)
        self.assertEqual(len(load_pattern(str(PATTERNS / "gosper_gun.txt"))), 36)


if __name__ == "__main__":
    unittest.main()
