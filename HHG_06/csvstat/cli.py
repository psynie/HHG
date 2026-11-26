from __future__ import annotations

import argparse
import sys
from typing import Optional, Sequence

from .histogram import histogram
from .reader import infer_column, is_missing, read_columns
from .stats import summarize_numeric, summarize_text


def fmt(value) -> str:
    return f"{value:.2f}" if isinstance(value, float) else str(value)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="csvstat", description="CSV summary statistics")
    parser.add_argument("file")
    parser.add_argument("--columns", help="comma-separated column names to include")
    parser.add_argument("--histogram", metavar="COLUMN", help="print a histogram of a numeric column")
    parser.add_argument("--bins", type=int, default=5)
    args = parser.parse_args(argv)

    try:
        columns = read_columns(args.file)
        wanted = args.columns.split(",") if args.columns else list(columns)
        unknown = [c for c in wanted if c not in columns]
        if unknown:
            raise ValueError(f"unknown column(s): {', '.join(unknown)}")

        if args.histogram:
            if args.histogram not in columns:
                raise ValueError(f"unknown column: {args.histogram}")
            kind, values = infer_column(columns[args.histogram])
            if kind != "numeric":
                raise ValueError(f"column '{args.histogram}' is not numeric")
            print(histogram(values, args.bins))
            return 0

        for name in wanted:
            raw = columns[name]
            missing = sum(is_missing(v) for v in raw)
            kind, values = infer_column(raw)
            print(f"{name} ({kind})")
            summary = (summarize_numeric(values, missing) if kind == "numeric"
                       else summarize_text(values, missing))
            for key, value in summary.items():
                print(f"  {key:<8}{fmt(value)}")
            print()
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0
