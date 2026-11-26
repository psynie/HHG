from __future__ import annotations

import argparse
import sys
from typing import Optional, Sequence

from .generator import generate_passphrase, generate_password
from .strength import check


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="passforge")
    sub = parser.add_subparsers(dest="command", required=True)

    gen = sub.add_parser("generate", help="generate a random password")
    gen.add_argument("--length", type=int, default=16)
    gen.add_argument("--no-lower", action="store_true")
    gen.add_argument("--no-upper", action="store_true")
    gen.add_argument("--no-digits", action="store_true")
    gen.add_argument("--no-symbols", action="store_true")

    phrase = sub.add_parser("passphrase", help="generate a word-based passphrase")
    phrase.add_argument("--words", type=int, default=4)
    phrase.add_argument("--separator", default="-")

    chk = sub.add_parser("check", help="rate the strength of a password")
    chk.add_argument("password")

    args = parser.parse_args(argv)
    try:
        if args.command == "generate":
            print(generate_password(
                args.length,
                lower=not args.no_lower, upper=not args.no_upper,
                digits=not args.no_digits, symbols=not args.no_symbols,
            ))
        elif args.command == "passphrase":
            print(generate_passphrase(args.words, args.separator))
        else:
            report = check(args.password)
            print(f"Entropy: {report.entropy_bits} bits ({report.rating})")
            for warning in report.warnings:
                print(f"  - {warning}")
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0
