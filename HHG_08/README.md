# HHG_08 — LeitnerCards

A command-line flashcard trainer using the Leitner spaced-repetition system.
Cards you know well appear less often; cards you miss come back quickly.

## How the Leitner system works here

Cards live in five boxes. A new card starts in box 1.

- Answer **correctly** and the card moves up one box
- Answer **incorrectly** and it drops back to box 1

Each box has a review interval: 1, 2, 4, 8 and 16 days for boxes 1 to 5.
A card is *due* when its next review date has arrived. Only due cards are
shown in a study session.

## Usage

```bash
python -m leitnercards import decks/python_basics.csv
python -m leitnercards study
python -m leitnercards study --limit 5
python -m leitnercards stats
```

Progress is stored in `~/.leitnercards.json` (override with `--file`).

During `study` you see the question, press Enter to reveal the answer, then
type `y` if you got it right or `n` if you did not.

## Layout

```
leitnercards/
  __init__.py
  __main__.py
  deck.py        # Card model, scheduling rules, JSON persistence
  importer.py    # CSV import (question,answer)
  session.py     # study-session loop with injectable input/output
  cli.py
decks/
  python_basics.csv
tests/
  test_deck.py
  test_session.py
```

## Running the tests

```bash
python -m unittest discover -s tests -v
```

The study loop takes its input and output functions as parameters, which is
how the tests drive a whole session without a terminal.
