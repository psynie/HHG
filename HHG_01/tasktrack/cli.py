from __future__ import annotations

import argparse
import sys
from typing import Optional, Sequence

from .models import PRIORITIES
from .storage import TaskStore


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tasktrack", description="Simple to-do manager")
    parser.add_argument("--file", help="path to the JSON task file")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="add a task")
    add.add_argument("title")
    add.add_argument("--priority", choices=PRIORITIES, default="medium")
    add.add_argument("--due", help="due date, YYYY-MM-DD")

    ls = sub.add_parser("list", help="list tasks")
    ls.add_argument("--status", choices=("all", "open", "done"), default="all")
    ls.add_argument("--priority", choices=PRIORITIES)

    done = sub.add_parser("done", help="mark a task as done")
    done.add_argument("id", type=int)

    rm = sub.add_parser("delete", help="delete a task")
    rm.add_argument("id", type=int)
    return parser


def format_task(task) -> str:
    box = "[x]" if task.done else "[ ]"
    due = f" (due {task.due})" if task.due else ""
    return f"{task.id:>3} {box} {task.priority:<6} {task.title}{due}"


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    store = TaskStore(args.file)
    try:
        if args.command == "add":
            task = store.add(args.title, args.priority, args.due)
            print(f"Added task {task.id}: {task.title}")
        elif args.command == "list":
            tasks = store.list(args.status, args.priority)
            if not tasks:
                print("No tasks found.")
            for task in tasks:
                print(format_task(task))
        elif args.command == "done":
            task = store.mark_done(args.id)
            print(f"Completed: {task.title}")
        elif args.command == "delete":
            store.delete(args.id)
            print(f"Deleted task {args.id}")
    except (KeyError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0
