import tempfile
import unittest
from pathlib import Path

from tasktrack.storage import TaskStore


class TaskStoreTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = Path(self.dir.name) / "tasks.json"

    def tearDown(self):
        self.dir.cleanup()

    def test_persists_between_instances(self):
        TaskStore(self.path).add("first")
        self.assertEqual(len(TaskStore(self.path).tasks), 1)

    def test_ids_are_not_reused(self):
        store = TaskStore(self.path)
        a = store.add("a")
        store.delete(a.id)
        b = store.add("b")
        self.assertEqual(b.id, a.id + 1)

    def test_filtering(self):
        store = TaskStore(self.path)
        store.add("a", "high")
        done = store.add("b", "low")
        store.mark_done(done.id)
        self.assertEqual([t.title for t in store.list("open")], ["a"])
        self.assertEqual([t.title for t in store.list(priority="low")], ["b"])

    def test_missing_id_raises(self):
        with self.assertRaises(KeyError):
            TaskStore(self.path).get(99)


if __name__ == "__main__":
    unittest.main()
