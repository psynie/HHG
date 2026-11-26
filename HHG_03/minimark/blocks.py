from __future__ import annotations

import html
import re
from typing import List

from .inline import render_inline

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
UL_RE = re.compile(r"^[-*]\s+(.*)$")
OL_RE = re.compile(r"^\d+\.\s+(.*)$")
HR_RE = re.compile(r"^(-{3,}|\*{3,})$")


def convert(markdown: str) -> str:
    lines = markdown.replace("\r\n", "\n").split("\n")
    out: List[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
        elif stripped.startswith("```"):
            i, block = _code_block(lines, i)
            out.append(block)
        elif HR_RE.match(stripped):
            out.append("<hr>")
            i += 1
        elif HEADING_RE.match(stripped):
            level, text = HEADING_RE.match(stripped).groups()
            out.append(f"<h{len(level)}>{render_inline(text)}</h{len(level)}>")
            i += 1
        elif stripped.startswith(">"):
            i, block = _quote(lines, i)
            out.append(block)
        elif UL_RE.match(stripped):
            i, block = _list(lines, i, UL_RE, "ul")
            out.append(block)
        elif OL_RE.match(stripped):
            i, block = _list(lines, i, OL_RE, "ol")
            out.append(block)
        else:
            i, block = _paragraph(lines, i)
            out.append(block)
    return "\n".join(out)


def _code_block(lines, i):
    i += 1
    body = []
    while i < len(lines) and not lines[i].strip().startswith("```"):
        body.append(lines[i])
        i += 1
    i += 1  # skip closing fence (or run off the end)
    return i, "<pre><code>" + html.escape("\n".join(body), quote=False) + "</code></pre>"


def _quote(lines, i):
    body = []
    while i < len(lines) and lines[i].strip().startswith(">"):
        body.append(lines[i].strip()[1:].strip())
        i += 1
    return i, "<blockquote>" + render_inline(" ".join(body)) + "</blockquote>"


def _list(lines, i, pattern, tag):
    items = []
    while i < len(lines) and pattern.match(lines[i].strip()):
        items.append(pattern.match(lines[i].strip()).group(1))
        i += 1
    inner = "".join(f"<li>{render_inline(item)}</li>" for item in items)
    return i, f"<{tag}>{inner}</{tag}>"


def _paragraph(lines, i):
    body = []
    while i < len(lines):
        s = lines[i].strip()
        if not s or s.startswith(("```", ">")) or HEADING_RE.match(s) \
                or UL_RE.match(s) or OL_RE.match(s) or HR_RE.match(s):
            break
        body.append(s)
        i += 1
    return i, "<p>" + render_inline(" ".join(body)) + "</p>"
