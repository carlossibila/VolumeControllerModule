"""Test script to check audio session discovery"""
from pycaw.pycaw import AudioUtilities

APPS = {
    0: "spotify",
    1: "discord",
    2: "brave"
}

print("=== All Active Audio Sessions ===")
sessions = AudioUtilities.GetAllSessions()
for session in sessions:
    if session.Process and session.State == 1:
        process_name = session.Process.name()
        print(f"- {process_name}")

print("\n=== Looking for target apps ===")
app_names_lower = {idx: name.lower() for idx, name in APPS.items()}

for session in sessions:
    if session.Process and session.State == 1:
        process_name = session.Process.name().lower()
        for idx, app_name in app_names_lower.items():
            if app_name in process_name:
                print(f"[OK] Found: {APPS[idx]} (process: {process_name})")
                break
