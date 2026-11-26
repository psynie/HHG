# HHG_03 — MiniMark

A lightweight Markdown-to-HTML converter written from scratch with the Python
standard library. It covers the subset of Markdown that most notes and READMEs
actually use.

## Supported syntax

- Headings `#` through `######`
- Paragraphs, with `**bold**`, `*italic*`, `` `inline code` `` and `[links](url)`
- Unordered lists (`-` or `*`) and ordered lists (`1.`)
- Fenced code blocks with triple backticks
- Block quotes (`>`)
- Horizontal rules (`---`)

All text is HTML-escaped before inline formatting is applied, so raw `<script>`
tags in the input are rendered as text, not executed.

## Usage

```bash
python -m minimark examples/sample.md            # prints HTML to stdout
python -m minimark examples/sample.md -o out.html --full
```

`--full` wraps the output in a complete HTML page with a small stylesheet.

## Layout

```
minimark/
  __init__.py     # exposes convert()
  __main__.py
  inline.py       # bold / italic / code / link handling
  blocks.py       # block-level parsing (headings, lists, code, quotes)
  cli.py
examples/
  sample.md
tests/
  test_inline.py
  test_blocks.py
```

## Running the tests

```bash
python -m unittest discover -s tests -v
```

## Known limitations

No nested lists, tables, images, or reference-style links. Those are the
natural next features if you want to extend it.
