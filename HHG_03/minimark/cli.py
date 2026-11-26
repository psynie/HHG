from __future__ import annotations

import argparse
import sys
from typing import Optional, Sequence

from .blocks import convert

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
body {{ font-family: sans-serif; max-width: 42rem; margin: 2rem auto; line-height: 1.6; }}
pre {{ background: #f4f4f4; padding: 1rem; overflow-x: auto; }}
code {{ background: #f4f4f4; padding: 0 .2em; }}
blockquote {{ border-left: 4px solid #ccc; margin-left: 0; padding-left: 1rem; color: #555; }}
</style>
</head>
<body>
{body}
</body>
</html>
"""


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="minimark", description="Markdown to HTML")
    parser.add_argument("input", help="Markdown file")
    parser.add_argument("-o", "--output", help="write HTML here instead of stdout")
    parser.add_argument("--full", action="store_true", help="wrap in a full HTML page")
    args = parser.parse_args(argv)

    try:
        with open(args.input, encoding="utf-8") as fh:
            body = convert(fh.read())
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    result = PAGE.format(title=args.input, body=body) if args.full else body + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(result)
    else:
        sys.stdout.write(result)
    return 0
