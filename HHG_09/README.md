# HHG_09 — LifeSim

Conway's Game of Life in the terminal, with a few extras: pattern files, a
wrap-around (toroidal) world option, and simple statistics.

## The rules

On an infinite grid each cell is alive or dead. Every generation:

1. A live cell with 2 or 3 live neighbours survives
2. A dead cell with exactly 3 live neighbours becomes alive
3. Everything else dies or stays dead

This implementation stores only the set of live cells, so the world can grow
without a fixed array, and large empty areas cost nothing.

## Usage

```bash
python -m lifesim patterns/glider.txt --generations 20
python -m lifesim patterns/gosper_gun.txt --generations 60 --delay 0.05
python -m lifesim patterns/blinker.txt --generations 4 --no-clear
python -m lifesim patterns/glider.txt --torus 20x10
```

- `--torus WxH` runs on a W-by-H grid whose edges wrap around
- `--delay` seconds between frames (default 0.1)
- `--no-clear` prints frames one after another instead of redrawing in place

## Pattern file format

Plain text. `#` or `O` is a live cell; `.` is a dead cell. Lines starting with
`!` are comments.

```
! Glider
.O.
..O
OOO
```

## Layout

```
lifesim/
  __init__.py
  __main__.py
  world.py       # World class: step(), neighbours, torus support
  patterns.py    # pattern file parser
  render.py      # frame rendering and bounding box
  cli.py
patterns/
  glider.txt  blinker.txt  block.txt  gosper_gun.txt
tests/
  test_world.py
  test_patterns.py
```

## Running the tests

```bash
python -m unittest discover -s tests -v
```

The tests check known behaviour: a block never changes, a blinker has period
2, and a glider moves one cell diagonally every 4 generations.
