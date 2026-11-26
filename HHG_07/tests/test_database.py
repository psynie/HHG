import unittest

from shortlink.database import LinkDatabase


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.db = LinkDatabase()

    def tearDown(self):
        self.db.close()

    def test_same_url_same_code(self):
        a = self.db.shorten("https://example.com/x")
        b = self.db.shorten("https://example.com/x")
        self.assertEqual(a, b)

    def test_different_urls_different_codes(self):
        self.assertNotEqual(
            self.db.shorten("https://example.com/1"), self.db.shorten("https://example.com/2")
        )

    def test_resolve_counts_hits(self):
        code = self.db.shorten("https://example.com/x")
        self.assertEqual(self.db.resolve(code), "https://example.com/x")
        self.db.resolve(code)
        self.assertEqual(self.db.stats(code)["hits"], 2)

    def test_unknown_code(self):
        self.assertIsNone(self.db.resolve("zzzzzz"))
        self.assertIsNone(self.db.stats("zzzzzz"))

    def test_invalid_url_rejected(self):
        with self.assertRaises(ValueError):
            self.db.shorten("not a url")


if __name__ == "__main__":
    unittest.main()
