# HHG_02 — LogLens

A command-line analyzer for web server access logs in the Common Log Format
(the default for nginx and Apache).

## What it does

Reads one or more log files and reports:

- Total requests and total bytes served
- Requests per HTTP status class (2xx, 3xx, 4xx, 5xx)
- Top N client IPs and top N requested paths
- Requests per hour, so you can spot traffic spikes
- Lines that could not be parsed (counted, never silently dropped)

## Usage

```bash
python -m loglens samples/access.log
python -m loglens samples/access.log --top 5
python -m loglens samples/access.log --json > report.json
```

## Layout

```
loglens/
  __init__.py
  __main__.py
  parser.py      # regex parser for Common Log Format lines
  analyzer.py    # aggregates parsed entries into a report
  cli.py         # argparse front end, text and JSON output
samples/
  access.log     # small realistic sample to try it on
tests/
  test_parser.py
  test_analyzer.py
```

## Running the tests

```bash
python -m unittest discover -s tests -v
```

Requires Python 3.9+. No third-party packages.

## Log format

```
203.0.113.7 - - [26/Nov/2026:10:15:32 +0000] "GET /index.html HTTP/1.1" 200 5120
```

The `-` fields (identity and user) are accepted but ignored. A `-` for the
byte count is treated as zero.
