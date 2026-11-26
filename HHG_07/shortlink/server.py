from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .codes import is_valid_code
from .database import LinkDatabase

MAX_BODY = 8192


def make_server(host: str, port: int, db: LinkDatabase) -> ThreadingHTTPServer:
    class Handler(BaseHTTPRequestHandler):
        def _json(self, status: int, payload: dict) -> None:
            body = json.dumps(payload).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_POST(self):
            if self.path != "/shorten":
                return self._json(404, {"error": "not found"})
            length = int(self.headers.get("Content-Length") or 0)
            if length > MAX_BODY:
                return self._json(413, {"error": "request too large"})
            try:
                data = json.loads(self.rfile.read(length) or b"{}")
                code = db.shorten(str(data.get("url", "")))
            except (json.JSONDecodeError, ValueError) as exc:
                return self._json(400, {"error": str(exc)})
            host_header = self.headers.get("Host", f"{host}:{port}")
            self._json(200, {"code": code, "short_url": f"http://{host_header}/{code}"})

        def do_GET(self):
            if self.path.startswith("/stats/"):
                code = self.path[len("/stats/"):]
                info = db.stats(code) if is_valid_code(code) else None
                if info is None:
                    return self._json(404, {"error": "unknown code"})
                return self._json(200, info)
            code = self.path.lstrip("/")
            url = db.resolve(code) if is_valid_code(code) else None
            if url is None:
                return self._json(404, {"error": "unknown code"})
            self.send_response(302)
            self.send_header("Location", url)
            self.send_header("Content-Length", "0")
            self.end_headers()

        def log_message(self, fmt, *args):  # keep test output quiet
            pass

    return ThreadingHTTPServer((host, port), Handler)
