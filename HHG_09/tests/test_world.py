import unittest
from pathlib import Path

from lifesim.patterns import load_pattern
from lifesim.render import render
from lifesim.world import World

PATTERNS = Path(__file__).resolve().parent.parent / "patterns"


class WorldTests(unittest.TestCase):
    def test_block_is_stable(self):
        world = World(load_pattern(str(PATTERNS / "block.txt")))
        before = set(world.live)
        world.run(5)
        self.assertEqual(world.live, before)

    def test_blinker_has_period_two(self):
        world = World(load_pattern(str(PATTERNS / "blinker.txt")))
        start = set(world.live)
        world.step()
        self.assertNotEqual(world.live, start)
        world.step()
        self.assertEqual(world.live, start)

    def test_glider_moves_diagonally(self):
        start = load_pattern(str(PATTERNS / "glider.txt"))
        world = World(start)
        world.run(4)
        self.assertEqual(world.live, {(x + 1, y + 1) for x, y in start})

    def test_lonely_cell_dies(self):
        world = World({(0, 0)})
        world.step()
        self.assertEqual(len(world), 0)

    def test_torus_glider_returns_home(self):
        # On a 6x6 torus a glider travels (1,1) per 4 steps, so 24 steps = 6 cells = full lap.
        start = load_pattern(str(PATTERNS / "glider.txt"))
        world = World(start, size=(6, 6))
        world.run(24)
        self.assertEqual(world.live, set(start))

    def test_gosper_gun_grows(self):
        world = World(load_pattern(str(PATTERNS / "gosper_gun.txt")))
        initial = len(world)
        world.run(120)
        self.assertGreater(len(world), initial)

    def test_render_empty(self):
        self.assertEqual(render(World()), "(empty world)")


if __name__ == "__main__":
    unittest.main()
