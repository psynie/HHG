from __future__ import annotations

from collections import Counter
from typing import Iterable, Optional, Set, Tuple

Cell = Tuple[int, int]  # (x, y)

OFFSETS = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx, dy) != (0, 0)]


class World:
    """A Game of Life world holding only its live cells.

    If `size=(width, height)` is given the world is a torus: coordinates wrap
    around the edges. Otherwise the grid is unbounded.
    """

    def __init__(self, live: Iterable[Cell] = (), size: Optional[Tuple[int, int]] = None):
        self.size = size
        self.generation = 0
        self.live: Set[Cell] = {self._wrap(c) for c in live}

    def _wrap(self, cell: Cell) -> Cell:
        if self.size is None:
            return cell
        return (cell[0] % self.size[0], cell[1] % self.size[1])

    def step(self) -> None:
        # Count, for every cell next to a live cell, how many live neighbours it has.
        counts = Counter(
            self._wrap((x + dx, y + dy)) for (x, y) in self.live for dx, dy in OFFSETS
        )
        self.live = {
            cell for cell, n in counts.items()
            if n == 3 or (n == 2 and cell in self.live)
        }
        self.generation += 1

    def run(self, generations: int) -> None:
        for _ in range(generations):
            self.step()

    def __len__(self) -> int:
        return len(self.live)

    def bounds(self) -> Optional[Tuple[int, int, int, int]]:
        """Return (min_x, min_y, max_x, max_y) of live cells, or None if empty."""
        if not self.live:
            return None
        xs = [x for x, _ in self.live]
        ys = [y for _, y in self.live]
        return min(xs), min(ys), max(xs), max(ys)
