"""Force-stop all automation processes launched by .py/.bat/.ps1 files in
this directory. Python port of stop.ps1.

Uses PowerShell's Get-CimInstance (reliable on Windows 10/11) to enumerate
processes and their command lines, then taskkill /F /PID matches.

Invoked by stop.bat (which activates the venv and runs `python stop.py`).
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys


SELF_NAMES = {"stop.py", "stop.bat", "stop.ps1"}


def ps_processes(name: str) -> list[dict]:
    """Return [{ProcessId, CommandLine}, ...] for every process whose image
    name equals `name` (e.g. 'python.exe')."""
    ps_cmd = (
        f"Get-CimInstance Win32_Process -Filter \"Name='{name}'\" "
        f"| Select-Object ProcessId,CommandLine "
        f"| ConvertTo-Json -Compress"
    )
    try:
        raw = subprocess.check_output(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
             "-Command", ps_cmd],
            stderr=subprocess.DEVNULL,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"  [debug] powershell query failed for {name}: {e}")
        return []

    text = raw.decode("utf-8", errors="ignore").strip()
    if not text:
        return []

    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        print(f"  [debug] JSON parse failed for {name}: {e}")
        return []

    # ConvertTo-Json emits a single object when there is exactly one match.
    if isinstance(data, dict):
        data = [data]
    return data


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
    procs = ps_processes(proc_name)
    print(f"  [debug] {proc_name}: {len(procs)} process(es), "
          f"{len(files)} local *.{ext} file(s)")

    if not files or not procs:
        print(f"No {label} processes found.")
        return

    pattern = re.compile(
        "|".join(re.escape(f) for f in files), re.IGNORECASE
    )

    found = False
    for proc in procs:
        pid = proc.get("ProcessId")
        cmdline = proc.get("CommandLine") or ""
        if not isinstance(pid, int):
            continue
        if not pattern.search(cmdline):
            continue
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
    sweep("pythonw.exe", "py", "PythonW", script_dir)
    print()
    sweep("powershell.exe", "ps1", "PowerShell", script_dir)
    print()
    sweep("cmd.exe", "bat", "CMD", script_dir)

    print()
    print("All automation processes have been terminated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
