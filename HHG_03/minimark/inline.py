from __future__ import annotations

import html
import re

CODE_RE = re.compile(r"`([^`]+)`")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
ITALIC_RE = re.compile(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")


def render_inline(text: str) -> str:
    """Escape HTML, then apply inline formatting.

    Inline code spans are pulled out first so their contents are never
    touched by the bold/italic/link rules.
    """
    escaped = html.escape(text, quote=False)
    stash = []

    def hold(match):
        stash.append(f"<code>{match.group(1)}</code>")
        return f"\x00{len(stash) - 1}\x00"

    escaped = CODE_RE.sub(hold, escaped)
    escaped = BOLD_RE.sub(r"<strong>\1</strong>", escaped)
    escaped = ITALIC_RE.sub(r"<em>\1</em>", escaped)
    escaped = LINK_RE.sub(_link, escaped)
    return re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], escaped)


def _link(match) -> str:
    label, url = match.group(1), match.group(2)
    if url.lower().startswith("javascript:"):
        return label
    return f'<a href="{html.escape(url, quote=True)}">{label}</a>'
