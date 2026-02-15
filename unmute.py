import os
from pycaw.pycaw import AudioUtilities

device = AudioUtilities.GetSpeakers()
volume = device.EndpointVolume

# Restore volume from backup file
backup_file = "volume_backup.txt"
if os.path.exists(backup_file):
    with open(backup_file, "r") as f:
        saved_volume = float(f.read().strip())
    volume.SetMasterVolumeLevelScalar(saved_volume, None)
    os.remove(backup_file)
    print(f"Volume restored to {int(saved_volume * 100)}%.")
else:
    # Default to 50% if no backup found
    volume.SetMasterVolumeLevelScalar(0.5, None)
    print("No volume backup found. Volume set to 50%.")
