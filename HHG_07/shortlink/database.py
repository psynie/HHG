from __future__ import annotations

import sqlite3
import threading
from datetime import datetime, timezone
from typing import Optional

from .codes import new_code, validate_url

SCHEMA = """
CREATE TABLE IF NOT EXISTS links (
    code       TEXT PRIMARY KEY,
    url        TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL,
    hits       INTEGER NOT NULL DEFAULT 0
)
"""


class LinkDatabase:
    def __init__(self, path: str = ":memory:"):
        # The HTTP server may call from several threads, so share one guarded connection.
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._lock = threading.Lock()
        with self._lock:
            self._conn.execute(SCHEMA)
            self._conn.commit()

    def close(self) -> None:
        with self._lock:
            self._conn.close()

    def shorten(self, url: str) -> str:
        url = validate_url(url)
        with self._lock:
            row = self._conn.execute("SELECT code FROM links WHERE url = ?", (url,)).fetchone()
            if row:
                return row["code"]
            while True:
                code = new_code()
                try:
                    self._conn.execute(
                        "INSERT INTO links (code, url, created_at) VALUES (?, ?, ?)",
                        (code, url, datetime.now(timezone.utc).isoformat(timespec="seconds")),
                    )
                    self._conn.commit()
                    return code
                except sqlite3.IntegrityError:
                    continue  # code collision, try another

    def resolve(self, code: str) -> Optional[str]:
        """Return the target URL and count the visit, or None if unknown."""
        with self._lock:
            row = self._conn.execute("SELECT url FROM links WHERE code = ?", (code,)).fetchone()
            if not row:
                return None
            self._conn.execute("UPDATE links SET hits = hits + 1 WHERE code = ?", (code,))
            self._conn.commit()
            return row["url"]

    def stats(self, code: str) -> Optional[dict]:
        with self._lock:
            row = self._conn.execute(
                "SELECT code, url, created_at, hits FROM links WHERE code = ?", (code,)
            ).fetchone()
        return dict(row) if row else None
