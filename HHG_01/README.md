# HHG_01 — TaskTrack

A small command-line to-do manager that stores tasks in a local JSON file.

## What it does

- Add tasks with an optional priority (`low`, `medium`, `high`) and due date
- List tasks, filtered by status or priority, sorted by due date and priority
- Mark tasks done, edit them, or delete them
- Data lives in `~/.tasktrack.json` by default (override with `--file` or `TASKTRACK_FILE`)

## Usage

```bash
python -m tasktrack add "Write report" --priority high --due 2026-12-01
python -m tasktrack list
python -m tasktrack list --status open --priority high
python -m tasktrack done 1
python -m tasktrack delete 1
```

## Layout

```
tasktrack/
  __init__.py
  __main__.py     # enables `python -m tasktrack`
  models.py       # Task dataclass and validation
  storage.py      # JSON load/save
  cli.py          # argparse front end
tests/
  test_storage.py
  test_models.py
```

## Running the tests

```bash
python -m unittest discover -s tests -v
```

Requires Python 3.9+. No third-party packages.

## Design notes

Tasks get an auto-incrementing integer ID that is never reused, so IDs in
your notes stay valid after deletions. Writes go to a temp file first and are
then renamed, so a crash mid-write cannot corrupt the task file.
