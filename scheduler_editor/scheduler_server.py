"""Serves scheduler.html and provides save endpoint for scheduler.json"""
import json
import os
import subprocess
import sys
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
GIT_REL_PATH = "scheduler_editor/scheduler.json"


def _run_git_sync():
    """git add/commit/push scheduler.json, then gitpull.bat on remotes."""
    sections = []

    def run_cmd(label, args, shell=False):
        r = subprocess.run(
            args,
            cwd=REPO_ROOT,
            shell=shell,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=600,
        )
        out = (r.stdout or "").rstrip()
        err = (r.stderr or "").rstrip()
        body = []
        if out:
            body.append(out)
        if err:
            body.append(err)
        block = "\n".join(body) if body else "(no output)"
        section = f"--- {label} (exit {r.returncode}) ---\n{block}"
        sections.append(section)
        print(section + "\n", flush=True)
        return r.returncode

    code = run_cmd("git add", ["git", "add", GIT_REL_PATH])
    if code != 0:
        return False, "git add failed", "\n\n".join(sections)

    code = run_cmd('git commit -m "update scheduler"', ["git", "commit", "-m", "update scheduler"])
    # 1 = nothing to commit (file unchanged); still try push + pull
    if code not in (0, 1):
        return False, "git commit failed", "\n\n".join(sections)

    code = run_cmd("git push", ["git", "push"])
    if code != 0:
        return False, "git push failed", "\n\n".join(sections)

    bat = os.path.join(REPO_ROOT, "gitpull.bat")
    if not os.path.isfile(bat):
        return True, "saved and pushed (gitpull.bat missing)", "\n\n".join(sections)

    code = run_cmd("gitpull.bat", ["cmd", "/c", "gitpull.bat", "nopause"], shell=False)
    if code != 0:
        return False, "gitpull.bat failed", "\n\n".join(sections)

    return True, "saved, pushed, and pulled on remotes", "\n\n".join(sections)


def _run_restart_scheduler_bat():
    """Run restart_scheduler.bat (SSH remotes + scheduler_restart on each)."""
    bat = os.path.join(REPO_ROOT, "restart_scheduler.bat")
    if not os.path.isfile(bat):
        return False, "--- restart_scheduler.bat (missing) ---\n(not found)", ""
    r = subprocess.run(
        ["cmd", "/c", "restart_scheduler.bat", "nopause"],
        cwd=REPO_ROOT,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=900,
    )
    out = (r.stdout or "").rstrip()
    err = (r.stderr or "").rstrip()
    body = []
    if out:
        body.append(out)
    if err:
        body.append(err)
    block = "\n".join(body) if body else "(no output)"
    section = f"--- restart_scheduler.bat (exit {r.returncode}) ---\n{block}"
    print(section + "\n", flush=True)
    ok = r.returncode == 0
    return ok, section


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
                try:
                    sync_ok, msg, log = _run_git_sync()
                except subprocess.TimeoutExpired:
                    sync_ok, msg, log = False, "git sync timed out", ""
                except OSError as e:
                    sync_ok, msg, log = False, f"sync failed: {e}", ""
                try:
                    restart_ok, restart_section = _run_restart_scheduler_bat()
                except subprocess.TimeoutExpired:
                    restart_ok, restart_section = False, "--- restart_scheduler.bat (timeout) ---"
                except OSError as e:
                    restart_ok, restart_section = False, f"restart_scheduler.bat failed: {e}"
                parts = [p for p in (log, restart_section) if p]
                full_log = "\n\n".join(parts) if parts else None
                if restart_ok:
                    msg = f"{msg}; restart_scheduler.bat completed"
                else:
                    msg = f"{msg}; restart_scheduler.bat failed"
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(
                    json.dumps(
                        {
                            "ok": True,
                            "sync": sync_ok,
                            "restart": restart_ok,
                            "message": msg,
                            "log": full_log,
                        }
                    ).encode()
                )
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
