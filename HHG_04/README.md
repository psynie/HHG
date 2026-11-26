# HHG_04 — SplitWise Lite

A tool for settling shared expenses in a group (a trip, a flat, a dinner).
Record who paid for what, and it works out the smallest set of payments that
leaves everyone even.

## How it works

1. Each expense has a payer, an amount, and the people who share it.
2. The tool computes every person's net balance (paid minus owed).
3. A greedy settlement matches the biggest debtor with the biggest creditor
   until all balances are zero. This yields at most *n − 1* payments for *n*
   people.

All money is handled as integer cents to avoid floating-point rounding errors.
When an amount does not divide evenly, the leftover cents go to the first
people in the share list, so the totals always add up exactly.

## Usage

Describe the group in a JSON file (see `examples/trip.json`) and run:

```bash
python -m splitlite examples/trip.json
```

Sample output:

```
Balances:
  Asha       +80.00
  Ben        -25.00
  Chitra     -55.00

Settlements:
  Chitra pays Asha 55.00
  Ben pays Asha 25.00
```

## Layout

```
splitlite/
  __init__.py
  __main__.py
  ledger.py      # expenses, balances, cent-accurate splitting
  settle.py      # minimal-payment settlement algorithm
  cli.py
examples/
  trip.json
tests/
  test_ledger.py
  test_settle.py
```

## Running the tests

```bash
python -m unittest discover -s tests -v
```
