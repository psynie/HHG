# HHG_06 — CsvStat

Quick descriptive statistics for CSV files, from the command line, with no
pandas required.

## What it does

For every column in a CSV file, CsvStat decides whether it is numeric or text
and reports:

- **Numeric columns:** count, missing values, min, max, mean, median, standard
  deviation, and the 25th/75th percentiles
- **Text columns:** count, missing values, number of unique values, and the
  most common values

It can also select columns and print a plain-text histogram for a numeric one.

## Usage

```bash
python -m csvstat data/students.csv
python -m csvstat data/students.csv --columns score,age
python -m csvstat data/students.csv --histogram score --bins 6
```

## Layout

```
csvstat/
  __init__.py
  __main__.py
  reader.py       # CSV loading and column type inference
  stats.py        # numeric and text summaries, percentiles
  histogram.py    # ASCII histogram
  cli.py
data/
  students.csv    # sample dataset
tests/
  test_stats.py
  test_reader.py
```

## Running the tests

```bash
python -m unittest discover -s tests -v
```

## Notes

A column counts as numeric when every non-empty value parses as a number.
Empty strings, `NA`, `N/A` and `null` are treated as missing. Percentiles use
linear interpolation, matching NumPy's default.
