import math
import unittest

from csvstat.histogram import histogram
from csvstat.stats import percentile, summarize_numeric, summarize_text


class StatsTests(unittest.TestCase):
    def test_percentile_interpolates(self):
        data = [1, 2, 3, 4]
        self.assertEqual(percentile(data, 50), 2.5)
        self.assertEqual(percentile(data, 0), 1)
        self.assertEqual(percentile(data, 100), 4)

    def test_numeric_summary(self):
        s = summarize_numeric([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])
        self.assertEqual(s["mean"], 5.0)
        self.assertEqual(s["median"], 4.5)
        self.assertAlmostEqual(s["std"], 2.138, places=3)

    def test_single_value_std_is_nan(self):
        self.assertTrue(math.isnan(summarize_numeric([3.0])["std"]))

    def test_text_summary(self):
        s = summarize_text(["a", "b", "a"], missing=1)
        self.assertEqual(s["unique"], 2)
        self.assertEqual(s["top"][0], ("a", 2))
        self.assertEqual(s["missing"], 1)

    def test_histogram_counts_sum(self):
        out = histogram([1, 2, 3, 4, 5, 6], bins=3)
        counts = [int(line.rsplit(" ", 1)[1]) for line in out.splitlines()]
        self.assertEqual(sum(counts), 6)

    def test_histogram_constant_values(self):
        self.assertIn("3", histogram([5, 5, 5], bins=2))


if __name__ == "__main__":
    unittest.main()
