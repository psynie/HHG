import unittest
from pathlib import Path

from csvstat.reader import infer_column, is_missing, read_columns

SAMPLE = Path(__file__).resolve().parent.parent / "data" / "students.csv"


class ReaderTests(unittest.TestCase):
    def test_missing_markers(self):
        for value in ("", " ", "NA", "n/a", "NULL"):
            self.assertTrue(is_missing(value))
        self.assertFalse(is_missing("0"))

    def test_infers_numeric_and_text(self):
        self.assertEqual(infer_column(["1", "2.5", ""])[0], "numeric")
        self.assertEqual(infer_column(["1", "x"])[0], "text")

    def test_all_missing_is_text(self):
        self.assertEqual(infer_column(["", "NA"]), ("text", []))

    def test_reads_sample(self):
        cols = read_columns(str(SAMPLE))
        self.assertEqual(list(cols), ["name", "age", "grade", "score"])
        self.assertEqual(len(cols["name"]), 10)
        kind, values = infer_column(cols["score"])
        self.assertEqual(kind, "numeric")
        self.assertEqual(len(values), 9)  # one score is missing


if __name__ == "__main__":
    unittest.main()
