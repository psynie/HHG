import string
import unittest

from passforge.generator import SYMBOLS, generate_passphrase, generate_password


class GeneratorTests(unittest.TestCase):
    def test_length(self):
        self.assertEqual(len(generate_password(24)), 24)

    def test_contains_every_class(self):
        for _ in range(50):
            pw = generate_password(8)
            self.assertTrue(any(c in string.ascii_lowercase for c in pw))
            self.assertTrue(any(c in string.ascii_uppercase for c in pw))
            self.assertTrue(any(c in string.digits for c in pw))
            self.assertTrue(any(c in SYMBOLS for c in pw))

    def test_no_symbols_option(self):
        pw = generate_password(40, symbols=False)
        self.assertFalse(any(c in SYMBOLS for c in pw))

    def test_too_short_rejected(self):
        with self.assertRaises(ValueError):
            generate_password(3)

    def test_all_classes_disabled_rejected(self):
        with self.assertRaises(ValueError):
            generate_password(10, lower=False, upper=False, digits=False, symbols=False)

    def test_passphrase_word_count(self):
        self.assertEqual(len(generate_passphrase(5).split("-")), 5)


if __name__ == "__main__":
    unittest.main()
