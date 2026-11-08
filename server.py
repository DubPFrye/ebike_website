"""Small LAN web server for the e-bike parts landing page.

Standard library only. Serves the files in this folder.

    python server.py              # port 8000 on all interfaces
    python server.py --port 8080
    python server.py --host 127.0.0.1   # this machine only
"""

import argparse
import functools
import http.server
import socket
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def lan_ip() -> str:
    """Best guess at this machine's LAN address (no traffic is sent)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--host", default="0.0.0.0", help="interface to bind (default: all)")
    parser.add_argument("--port", type=int, default=8000, help="port (default: 8000)")
    args = parser.parse_args()

    handler = functools.partial(Handler, directory=str(ROOT))
    with http.server.ThreadingHTTPServer((args.host, args.port), handler) as httpd:
        print(f"Serving {ROOT}")
        print(f"  This machine: http://localhost:{args.port}")
        if args.host == "0.0.0.0":
            print(f"  On your LAN:  http://{lan_ip()}:{args.port}")
        print("Press Ctrl+C to stop.", flush=True)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == "__main__":
    main()
