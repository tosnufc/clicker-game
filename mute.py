from pycaw.pycaw import AudioUtilities

device = AudioUtilities.GetSpeakers()
volume = device.EndpointVolume

# Save current volume level to a file so we can restore it later
current_volume = volume.GetMasterVolumeLevelScalar()
with open("volume_backup.txt", "w") as f:
    f.write(str(current_volume))

print(f"Current volume: {int(current_volume * 100)}%")

# Mute by setting volume to 0
volume.SetMasterVolumeLevelScalar(0.0, None)
print("Volume set to 0%.")
