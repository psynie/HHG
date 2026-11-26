from __future__ import annotations

import argparse
import json
import sys
from typing import Optional, Sequence

from .analyzer import analyze


def read_lines(paths):
    for path in paths:
        with open(path, encoding="utf-8", errors="replace") as fh:
            yield from fh


def render_text(report: dict) -> str:
    out = [
        f"Requests:  {report['total_requests']}",
        f"Bytes:     {report['total_bytes']}",
        f"Unparsed:  {report['unparsed_lines']}",
        "",
        "Status classes:",
    ]
    out += [f"  {k}: {v}" for k, v in report["status_classes"].items()]
    out += ["", "Top IPs:"]
    out += [f"  {n:>5}  {ip}" for ip, n in report["top_ips"]]
    out += ["", "Top paths:"]
    out += [f"  {n:>5}  {p}" for p, n in report["top_paths"]]
    out += ["", "Requests per hour:"]
    out += [f"  {h}  {n}" for h, n in report["requests_per_hour"].items()]
    return "\n".join(out)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="loglens", description="Analyze access logs")
    parser.add_argument("files", nargs="+", help="log files to read")
    parser.add_argument("--top", type=int, default=10, help="how many IPs/paths to show")
    parser.add_argument("--json", action="store_true", help="output JSON instead of text")
    args = parser.parse_args(argv)

    try:
        report = analyze(read_lines(args.files), top=args.top)
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(report, indent=2) if args.json else render_text(report))
    return 0
