import unittest

from loglens.parser import parse_line

GOOD = '203.0.113.7 - - [26/Nov/2026:10:15:32 +0000] "GET /about?x=1 HTTP/1.1" 200 4096'


class ParserTests(unittest.TestCase):
    def test_parses_fields(self):
        entry = parse_line(GOOD)
        self.assertEqual(entry.ip, "203.0.113.7")
        self.assertEqual(entry.method, "GET")
        self.assertEqual(entry.status, 200)
        self.assertEqual(entry.size, 4096)
        self.assertEqual(entry.time.hour, 10)

    def test_strips_query_string(self):
        self.assertEqual(parse_line(GOOD).path, "/about")

    def test_dash_bytes_is_zero(self):
        line = '1.2.3.4 - - [26/Nov/2026:10:15:32 +0000] "GET / HTTP/1.1" 304 -'
        self.assertEqual(parse_line(line).size, 0)

    def test_garbage_returns_none(self):
        self.assertIsNone(parse_line("not a log line"))

    def test_bad_timestamp_returns_none(self):
        line = '1.2.3.4 - - [99/Foo/2026:10:15:32 +0000] "GET / HTTP/1.1" 200 1'
        self.assertIsNone(parse_line(line))


if __name__ == "__main__":
    unittest.main()
