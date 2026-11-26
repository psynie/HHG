from __future__ import annotations

from typing import Optional

from .world import World


def render(world: World, margin: int = 1) -> str:
    """Draw the world as text. A torus shows its whole grid; otherwise the live area."""
    if world.size:
        min_x, min_y = 0, 0
        max_x, max_y = world.size[0] - 1, world.size[1] - 1
    else:
        box = world.bounds()
        if box is None:
            return "(empty world)"
        min_x, min_y, max_x, max_y = box
        min_x -= margin
        min_y -= margin
        max_x += margin
        max_y += margin

    rows = []
    for y in range(min_y, max_y + 1):
        rows.append("".join("O" if (x, y) in world.live else "." for x in range(min_x, max_x + 1)))
    return "\n".join(rows)


def status_line(world: World) -> str:
    return f"Generation {world.generation}   Alive: {len(world)}"
