import subprocess

result = subprocess.run(
    ["powershell", "-nologo", "-noprofile", "-command",
     "Get-WmiObject Win32_Process -Filter \"commandline like '%scheduler.bat%'\" | Select-Object ProcessId"],
    capture_output=True, text=True
)

lines = [l.strip() for l in result.stdout.splitlines() if l.strip().isdigit()]
if lines:
    print(f"RUNNING (PID {lines[0]})")
else:
    print("NOT RUNNING")
