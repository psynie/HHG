import unittest

from passforge.strength import check, has_sequence, pool_size


class StrengthTests(unittest.TestCase):
    def test_common_password_is_weak(self):
        report = check("password")
        self.assertEqual(report.rating, "weak")
        self.assertIn("appears on the common-password list", report.warnings)

    def test_sequence_detection(self):
        self.assertTrue(has_sequence("xx1234yy"))
        self.assertTrue(has_sequence("DCBA"))
        self.assertFalse(has_sequence("a1b2c3"))

    def test_repeats_flagged(self):
        self.assertTrue(any("repeated" in w for w in check("aaaXyz!9Qr#2").warnings))

    def test_pool_size(self):
        self.assertEqual(pool_size("abc"), 26)
        self.assertEqual(pool_size("aB3"), 62)

    def test_long_mixed_password_is_strong(self):
        report = check("kT9#vLq2@xRm7!Zw")
        self.assertEqual(report.rating, "strong")
        self.assertEqual(report.warnings, [])


if __name__ == "__main__":
    unittest.main()
