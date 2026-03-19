"""Serves scheduler.html and provides save endpoint for scheduler.json"""
import json
import os
import sys
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
server_ref = None


def _shutdown_server():
    """Call shutdown from another thread (required by HTTPServer)."""
    if server_ref:
        server_ref.shutdown()


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SCRIPT_DIR, **kwargs)

    def do_POST(self):
        if self.path == '/save_scheduler':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body)
                path = os.path.join(SCRIPT_DIR, 'scheduler.json')
                with open(path, 'w') as f:
                    json.dump(data, f, indent=2)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"ok":true}')
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path == '/exit' or self.path == '/exit/':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"ok":true}')
            threading.Thread(target=_shutdown_server, daemon=True).start()
        elif self.path == '/scheduler.json' or self.path.startswith('/scheduler.json?'):
            path = os.path.join(SCRIPT_DIR, 'scheduler.json')
            try:
                with open(path) as f:
                    body = f.read().encode()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
                self.send_header('Pragma', 'no-cache')
                self.end_headers()
                self.wfile.write(body)
            except Exception:
                self.send_error(404)
        else:
            super().do_GET()

    def log_message(self, format, *args):
        pass


def main():
    global server_ref
    port = 8765
    server_ref = HTTPServer(('127.0.0.1', port), Handler)
    print(f"Open http://127.0.0.1:{port}/scheduler.html")
    print("Press Enter in this window, or click Exit in the browser, to stop.")

    def wait_for_enter():
        try:
            input()
        except (EOFError, KeyboardInterrupt):
            pass
        _shutdown_server()

    t = threading.Thread(target=wait_for_enter, daemon=True)
    t.start()

    try:
        server_ref.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server_ref.server_close()
    sys.exit(0)


if __name__ == '__main__':
    main()
