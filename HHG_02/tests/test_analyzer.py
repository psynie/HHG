import unittest
from pathlib import Path

from loglens.analyzer import analyze

SAMPLE = Path(__file__).resolve().parent.parent / "samples" / "access.log"


class AnalyzerTests(unittest.TestCase):
    def setUp(self):
        with open(SAMPLE, encoding="utf-8") as fh:
            self.report = analyze(fh, top=3)

    def test_counts(self):
        self.assertEqual(self.report["total_requests"], 14)
        self.assertEqual(self.report["unparsed_lines"], 1)

    def test_status_classes(self):
        classes = self.report["status_classes"]
        self.assertEqual(classes["4xx"], 2)
        self.assertEqual(classes["5xx"], 1)
        self.assertEqual(classes["3xx"], 3)

    def test_top_ip(self):
        self.assertEqual(self.report["top_ips"][0], ("203.0.113.7", 3))

    def test_hours_are_sorted(self):
        hours = list(self.report["requests_per_hour"])
        self.assertEqual(hours, sorted(hours))

    def test_empty_input(self):
        report = analyze([])
        self.assertEqual(report["total_requests"], 0)


if __name__ == "__main__":
    unittest.main()
