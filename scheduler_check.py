import subprocess

result = subprocess.run(
    ["tasklist", "/v", "/fi", "IMAGENAME eq cmd.exe"],
    capture_output=True, text=True
)

for line in result.stdout.splitlines():
    if "Scheduler" in line:
        pid = line.split()[1]
        print(f"RUNNING (PID {pid})")
        break
else:
    print("NOT RUNNING")
