# HHG_05 — PassForge

A password generator and strength checker that uses Python's `secrets` module
(a cryptographically secure random source) rather than `random`.

## Features

- **Generate** random passwords with configurable length and character sets
- **Passphrases**: pick words from a word list, e.g. `copper-lantern-meadow-quartz`
- **Check** a password: estimates entropy in bits, flags common weaknesses
  (too short, single character class, repeated characters, sequences like
  `abcd` or `1234`, entries on a common-password list)
- Guarantees at least one character from every selected class

## Usage

```bash
python -m passforge generate --length 20
python -m passforge generate --length 16 --no-symbols
python -m passforge passphrase --words 5
python -m passforge check "Tr0ub4dor&3"
```

The checker never stores or logs the password it is given.

## Layout

```
passforge/
  __init__.py
  __main__.py
  generator.py    # random passwords and passphrases
  strength.py     # entropy estimate and weakness checks
  cli.py
data/
  common_passwords.txt
  words.txt
tests/
  test_generator.py
  test_strength.py
```

## Running the tests

```bash
python -m unittest discover -s tests -v
```

## Honest caveats

Entropy here is a simple estimate (length × log2 of the character pool). Real
attackers use dictionaries and patterns, so treat the score as a rough guide
and prefer long passphrases plus a password manager and two-factor sign-in.
The bundled word and common-password lists are short, for demonstration; swap
in larger ones (for example the EFF long word list) for real use.
