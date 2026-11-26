from __future__ import annotations

import argparse
import sys
import time
from typing import Optional, Sequence

from .patterns import load_pattern
from .render import render, status_line
from .world import World

CLEAR = "\033[H\033[J"


def parse_size(text: str):
    try:
        w, h = text.lower().split("x")
        size = (int(w), int(h))
    except ValueError:
        raise argparse.ArgumentTypeError("size must look like 20x10")
    if size[0] < 3 or size[1] < 3:
        raise argparse.ArgumentTypeError("torus must be at least 3x3")
    return size


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="lifesim", description="Conway's Game of Life")
    parser.add_argument("pattern", help="pattern file")
    parser.add_argument("--generations", type=int, default=30)
    parser.add_argument("--delay", type=float, default=0.1)
    parser.add_argument("--torus", type=parse_size, metavar="WxH")
    parser.add_argument("--no-clear", action="store_true", help="do not redraw in place")
    args = parser.parse_args(argv)

    try:
        world = World(load_pattern(args.pattern), size=args.torus)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    try:
        for _ in range(args.generations + 1):
            if not args.no_clear:
                sys.stdout.write(CLEAR)
            print(render(world))
            print(status_line(world))
            if world.generation < args.generations:
                world.step()
                if args.delay > 0 and not args.no_clear:
                    time.sleep(args.delay)
    except KeyboardInterrupt:
        pass
    return 0
