import http.client
import json
import threading
import unittest

from shortlink.database import LinkDatabase
from shortlink.server import make_server


class NoRedirect(http.client.HTTPConnection):
    """http.client never follows redirects, which is what we want here."""


class ServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = LinkDatabase()
        cls.server = make_server("127.0.0.1", 0, cls.db)  # port 0 = any free port
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.db.close()

    def request(self, method, path, body=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        conn.request(method, path, body=json.dumps(body) if body is not None else None)
        resp = conn.getresponse()
        data = resp.read()
        conn.close()
        return resp, data

    def test_full_flow(self):
        resp, data = self.request("POST", "/shorten", {"url": "https://example.com/page"})
        self.assertEqual(resp.status, 200)
        code = json.loads(data)["code"]

        resp, _ = self.request("GET", f"/{code}")
        self.assertEqual(resp.status, 302)
        self.assertEqual(resp.getheader("Location"), "https://example.com/page")

        resp, data = self.request("GET", f"/stats/{code}")
        self.assertEqual(json.loads(data)["hits"], 1)

    def test_bad_url_is_400(self):
        resp, _ = self.request("POST", "/shorten", {"url": "javascript:alert(1)"})
        self.assertEqual(resp.status, 400)

    def test_bad_json_is_400(self):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        conn.request("POST", "/shorten", body="{not json")
        self.assertEqual(conn.getresponse().status, 400)
        conn.close()

    def test_unknown_code_is_404(self):
        resp, _ = self.request("GET", "/zzzzzz")
        self.assertEqual(resp.status, 404)


if __name__ == "__main__":
    unittest.main()
