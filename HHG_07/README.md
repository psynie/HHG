# HHG_07 — ShortLink

A self-hosted URL shortener built on Python's standard library: an HTTP
server, a SQLite database, and nothing else to install.

## Features

- `POST /shorten` with a JSON body `{"url": "https://example.com/long/path"}`
  returns a short code
- `GET /<code>` redirects (HTTP 302) to the original URL and counts the visit
- `GET /stats/<code>` returns the target URL, creation time and hit count
- Codes are 6 characters of base62, generated with `secrets`
- Re-shortening a URL that already exists returns the same code
- Only `http` and `https` URLs are accepted

## Run it

```bash
python -m shortlink --port 8080 --db links.db
```

```bash
curl -X POST localhost:8080/shorten -d '{"url": "https://example.com/a/very/long/path"}'
# {"code": "aB3xK9", "short_url": "http://localhost:8080/aB3xK9"}

curl -i localhost:8080/aB3xK9
curl localhost:8080/stats/aB3xK9
```

## Layout

```
shortlink/
  __init__.py
  __main__.py
  database.py     # SQLite storage layer
  codes.py        # base62 code generation and URL validation
  server.py       # http.server request handler
tests/
  test_database.py
  test_codes.py
  test_server.py  # starts a real server on a free port
```

## Running the tests

```bash
python -m unittest discover -s tests -v
```

## Production notes

`http.server` is fine for learning and small internal use. For anything public
put it behind a reverse proxy, add rate limiting, and consider a blocklist for
abusive destinations.
