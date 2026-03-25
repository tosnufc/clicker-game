"""Reads scheduler.json and runs workflows on schedule."""
import json
import os
import subprocess
import sys
import time
import traceback
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_ROOT = os.path.dirname(SCRIPT_DIR)  # clicker root, where workflow .bat files live
JSON_PATH = os.path.join(SCRIPT_DIR, "scheduler.json")

# Windows: launch via `start` so the helper cmd exits immediately and the workflow is not tied
# to the scheduler's console/job (reduces hangs taking down later scheduled runs).
if sys.platform == "win32":
    _CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)
else:
    _CREATE_NO_WINDOW = 0


def get_last_octet():
    try:
        result = subprocess.run(
            ["ipconfig"], capture_output=True, text=True, creationflags=0x08000000
        )
        for line in result.stdout.splitlines():
            if "IPv4" in line and ":" in line:
                parts = line.split(":")[-1].strip().split(".")
                if len(parts) == 4:
                    return parts[-1]
    except Exception:
        pass
    return "0"


def log(msg, logfile):
    ts = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    try:
        with open(logfile, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


def load_schedule():
    try:
        with open(JSON_PATH) as f:
            return json.load(f)
    except Exception:
        return {"workflows": []}


def launch_workflow_bat(bat: str):
    """Start a workflow .bat in a separate process tree (Windows: detached via start)."""
    if sys.platform == "win32":
        # start "" /MIN cmd /c <bat> — outer cmd used by Popen exits right after start returns;
        # the workflow runs under a new minimized console, not as a child blocking the scheduler.
        args = ["cmd", "/c", "start", "", "/MIN", "cmd", "/c", bat]
        subprocess.Popen(
            args,
            cwd=WORKSPACE_ROOT,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=_CREATE_NO_WINDOW,
        )
    else:
        subprocess.Popen(
            ["cmd", "/c", bat],
            cwd=WORKSPACE_ROOT,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


def main():
    os.chdir(WORKSPACE_ROOT)
    last_octet = get_last_octet()
    logfile = os.path.join(SCRIPT_DIR, f"{last_octet}_scheduler.log")
    log("Scheduler started", logfile)
    last_run = None
    tick = 0

    while True:
        try:
            data = load_schedule()
            workflows = data.get("workflows", [])
            now = datetime.now()
            dow = (now.weekday() + 1) % 7
            time_str = now.strftime("%H:%M")

            if time_str != last_run:
                launched = False
                for w in workflows:
                    day_ok = w.get("day") is None or w.get("day") == dow
                    time_ok = w.get("time") == time_str
                    if day_ok and time_ok:
                        bat = w.get("bat", "")
                        if bat:
                            log(f"Launching {w.get('workflow', bat)}...", logfile)
                            launch_workflow_bat(bat)
                            launched = True
                if launched:
                    last_run = time_str

        except Exception:
            log(f"Scheduler loop error (continuing): {traceback.format_exc()}", logfile)

        tick += 1
        if tick >= 120:
            tick = 0
            log("Scheduler heartbeat (ok)", logfile)

        time.sleep(30)


if __name__ == "__main__":
    main()
