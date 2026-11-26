import unittest

from shortlink.codes import is_valid_code, new_code, validate_url


class CodeTests(unittest.TestCase):
    def test_new_code_shape(self):
        for _ in range(100):
            self.assertTrue(is_valid_code(new_code()))

    def test_invalid_codes(self):
        for bad in ("", "abc", "abc12!", "toolongcode"):
            self.assertFalse(is_valid_code(bad))

    def test_validate_accepts_http_and_https(self):
        self.assertEqual(validate_url(" https://example.com/a "), "https://example.com/a")
        validate_url("http://example.com")

    def test_validate_rejects_bad_urls(self):
        for bad in ("", "ftp://x.com", "javascript:alert(1)", "example.com", "http://"):
            with self.assertRaises(ValueError):
                validate_url(bad)


if __name__ == "__main__":
    unittest.main()
