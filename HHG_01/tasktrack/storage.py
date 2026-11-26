from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import List, Optional

from .models import Task


class TaskStore:
    """Loads and saves tasks to a JSON file."""

    def __init__(self, path: Optional[os.PathLike] = None):
        default = os.environ.get("TASKTRACK_FILE") or Path.home() / ".tasktrack.json"
        self.path = Path(path or default)
        self.tasks: List[Task] = []
        self.next_id = 1
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        self.tasks = [Task.from_dict(t) for t in raw.get("tasks", [])]
        self.next_id = raw.get("next_id", max((t.id for t in self.tasks), default=0) + 1)

    def save(self) -> None:
        payload = {"next_id": self.next_id, "tasks": [t.to_dict() for t in self.tasks]}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=self.path.parent, suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)
        os.replace(tmp, self.path)

    def add(self, title: str, priority: str = "medium", due: Optional[str] = None) -> Task:
        task = Task(self.next_id, title, priority, due)
        self.next_id += 1
        self.tasks.append(task)
        self.save()
        return task

    def get(self, task_id: int) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise KeyError(f"no task with id {task_id}")

    def mark_done(self, task_id: int) -> Task:
        task = self.get(task_id)
        task.done = True
        self.save()
        return task

    def delete(self, task_id: int) -> None:
        task = self.get(task_id)
        self.tasks.remove(task)
        self.save()

    def list(self, status: str = "all", priority: Optional[str] = None) -> List[Task]:
        result = self.tasks
        if status == "open":
            result = [t for t in result if not t.done]
        elif status == "done":
            result = [t for t in result if t.done]
        if priority:
            result = [t for t in result if t.priority == priority]
        return sorted(result, key=Task.sort_key)
