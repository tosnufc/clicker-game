"""Reads scheduler.json and runs workflows on schedule."""
import json
import os
import subprocess
import time
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_ROOT = os.path.dirname(SCRIPT_DIR)  # clicker root, where workflow .bat files live
JSON_PATH = os.path.join(SCRIPT_DIR, 'scheduler.json')


def get_last_octet():
    try:
        result = subprocess.run(
            ['ipconfig'], capture_output=True, text=True, creationflags=0x08000000
        )
        for line in result.stdout.splitlines():
            if 'IPv4' in line and ':' in line:
                parts = line.split(':')[-1].strip().split('.')
                if len(parts) == 4:
                    return parts[-1]
    except Exception:
        pass
    return '0'


def log(msg, logfile):
    ts = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    line = f'[{ts}] {msg}'
    print(line)
    try:
        with open(logfile, 'a') as f:
            f.write(line + '\n')
    except Exception:
        pass


def load_schedule():
    try:
        with open(JSON_PATH) as f:
            return json.load(f)
    except Exception:
        return {'workflows': []}


def main():
    os.chdir(WORKSPACE_ROOT)
    last_octet = get_last_octet()
    logfile = os.path.join(SCRIPT_DIR, f'{last_octet}_scheduler.log')
    log('Scheduler started', logfile)
    last_run = None

    while True:
        data = load_schedule()
        workflows = data.get('workflows', [])
        now = datetime.now()
        dow = (now.weekday() + 1) % 7
        time_str = now.strftime('%H:%M')

        if time_str != last_run:
            launched = False
            for w in workflows:
                day_ok = w.get('day') is None or w.get('day') == dow
                time_ok = w.get('time') == time_str
                if day_ok and time_ok:
                    bat = w.get('bat', '')
                    if bat:
                        log(f"Launching {w.get('workflow', bat)}...", logfile)
                        subprocess.Popen(['cmd', '/c', bat], cwd=WORKSPACE_ROOT)
                        launched = True
            if launched:
                last_run = time_str

        time.sleep(30)


if __name__ == '__main__':
    main()
