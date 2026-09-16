"""Force-stop all automation processes launched by .py/.bat/.ps1 files in
this directory. Python port of stop.ps1 — parsing WMIC output in Python is
far more reliable than parsing it in cmd.exe.

Invoked by stop.bat (which activates the venv and runs `python stop.py`).
"""

from __future__ import annotations

import os
import re
import subprocess
import sys


SELF_NAMES = {"stop.py", "stop.bat", "stop.ps1"}


def wmic_processes(name: str) -> list[dict[str, str]]:
    """Return list of {CommandLine, ProcessId, ...} dicts for processes
    whose image name equals `name` (e.g. 'python.exe')."""
    try:
        raw = subprocess.check_output(
            [
                "wmic", "process",
                "where", f"name='{name}'",
                "get", "processid,commandline",
                "/format:list",
            ],
            stderr=subprocess.DEVNULL,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []

    # wmic emits UTF-16 on some systems; try utf-8 then fall back.
    for enc in ("utf-8", "utf-16", "mbcs"):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        text = raw.decode("utf-8", errors="ignore")

    records: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip().lstrip("\ufeff")
        if not line:
            if current:
                records.append(current)
                current = {}
            continue
        if "=" in line:
            k, v = line.split("=", 1)
            current[k.strip()] = v.strip()
    if current:
        records.append(current)
    return records


def taskkill(pid: int) -> bool:
    result = subprocess.run(
        ["taskkill", "/F", "/PID", str(pid)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def sweep(proc_name: str, ext: str, label: str, script_dir: str) -> None:
    files = [
        f for f in os.listdir(script_dir)
        if f.lower().endswith("." + ext) and f.lower() not in SELF_NAMES
    ]
    if not files:
        print(f"No {label} processes found.")
        return

    pattern = re.compile(
        "|".join(re.escape(f) for f in files), re.IGNORECASE
    )

    found = False
    for proc in wmic_processes(proc_name):
        pid_str = proc.get("ProcessId", "")
        cmdline = proc.get("CommandLine", "") or ""
        if not pid_str.isdigit():
            continue
        if not pattern.search(cmdline):
            continue
        pid = int(pid_str)
        # Extra safety: never kill our own interpreter or launcher.
        if pid == os.getpid() or pid == os.getppid():
            continue
        print(f"Stopping {label} process (PID: {pid})")
        print(f"  Command: {cmdline}")
        taskkill(pid)
        found = True

    if found:
        print(f"{label} processes stopped.")
    else:
        print(f"No {label} processes found.")


def main() -> int:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Stopping all automation processes from {script_dir}...")
    print()

    sweep("python.exe", "py", "Python", script_dir)
    print()
    sweep("powershell.exe", "ps1", "PowerShell", script_dir)
    print()
    # Also match pythonw.exe (windowless python) in case any script uses it.
    sweep("pythonw.exe", "py", "PythonW", script_dir)
    print()
    sweep("cmd.exe", "bat", "CMD", script_dir)

    print()
    print("All automation processes have been terminated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
