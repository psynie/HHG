import argparse

from .database import LinkDatabase
from .server import make_server


def main() -> None:
    parser = argparse.ArgumentParser(prog="shortlink")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--db", default="links.db")
    args = parser.parse_args()

    server = make_server(args.host, args.port, LinkDatabase(args.db))
    print(f"Serving on http://{args.host}:{server.server_address[1]}  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
