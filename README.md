# HHG

A collection of nine small, self-contained Python projects. Each lives in its
own folder with its own README, source code, sample data and tests. None of
them need third-party packages; Python 3.9 or newer is enough.

| Folder | Project | What it is |
|--------|---------|------------|
| [HHG_01](HHG_01) | TaskTrack | Command-line to-do manager with JSON storage |
| [HHG_02](HHG_02) | LogLens | Web server access-log analyzer |
| [HHG_03](HHG_03) | MiniMark | Markdown to HTML converter written from scratch |
| [HHG_04](HHG_04) | SplitWise Lite | Group expense splitter with minimal settlements |
| [HHG_05](HHG_05) | PassForge | Secure password generator and strength checker |
| [HHG_06](HHG_06) | CsvStat | Descriptive statistics for CSV files |
| [HHG_07](HHG_07) | ShortLink | Self-hosted URL shortener (HTTP server + SQLite) |
| [HHG_08](HHG_08) | LeitnerCards | Spaced-repetition flashcard trainer |
| [HHG_09](HHG_09) | LifeSim | Conway's Game of Life for the terminal |

## Running a project's tests

```bash
cd HHG_01
python -m unittest discover -s tests -v
```

Every project follows the same layout: a package folder, a `tests/` folder,
and a README with usage examples.
