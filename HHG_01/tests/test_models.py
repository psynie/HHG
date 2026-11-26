import unittest

from tasktrack.models import Task


class TaskModelTests(unittest.TestCase):
    def test_rejects_empty_title(self):
        with self.assertRaises(ValueError):
            Task(1, "   ")

    def test_rejects_bad_priority(self):
        with self.assertRaises(ValueError):
            Task(1, "x", priority="urgent")

    def test_rejects_bad_date(self):
        with self.assertRaises(ValueError):
            Task(1, "x", due="2026-13-45")

    def test_sort_puts_done_last(self):
        open_task = Task(1, "a", due="2026-12-01")
        done_task = Task(2, "b", due="2026-01-01", done=True)
        self.assertLess(open_task.sort_key(), done_task.sort_key())

    def test_roundtrip(self):
        task = Task(3, "write", "high", "2026-12-02")
        self.assertEqual(Task.from_dict(task.to_dict()), task)


if __name__ == "__main__":
    unittest.main()
