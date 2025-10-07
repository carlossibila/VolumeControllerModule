import serial
import pyautogui
import threading
import queue
import time
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

class VolumeController:
    def __init__(self, port='COM3', baudrate=250000):
        self.APPS = {
            0: "spotify",
            1: "discord",
            2: "brave"  # Default, can be changed via set_app()
        }
        # Pre-compile lowercase app names
        self.app_names_lower = {idx: name.lower() for idx, name in self.APPS.items()}

        self.arduino = serial.Serial(port, baudrate, timeout=0.001)
        self.last_volumes = [-1, -1, -1]
        self.running = True

        # Session cache
        self.session_cache = {}
        self.last_session_refresh = 0
        self.session_refresh_interval = 1.0  # Refresh every 1 second

        # Force initial session discovery
        self._refresh_sessions(force=True)

        # Volume change queue for decoupling
        self.volume_queue = queue.Queue()

        # Start volume processor thread
        self.volume_thread = threading.Thread(target=self._process_volume_changes, daemon=True)
        self.volume_thread.start()

    def _refresh_sessions(self, force=False):
        """Refresh audio session cache"""
        current_time = time.time()
        if force or current_time - self.last_session_refresh >= self.session_refresh_interval:
            self.session_cache.clear()
            sessions = AudioUtilities.GetAllSessions()

            for session in sessions:
                if session.Process and session.State == 1:  # Active session
                    process_name = session.Process.name().lower()
                    for idx, app_name in self.app_names_lower.items():
                        if app_name in process_name:
                            self.session_cache[idx] = session.SimpleAudioVolume
                            break

            self.last_session_refresh = current_time

    def _process_volume_changes(self):
        """Background thread to process volume changes from queue"""
        while self.running:
            try:
                app_idx, volume = self.volume_queue.get(timeout=0.1)
                self._refresh_sessions()

                if app_idx in self.session_cache:
                    self.session_cache[app_idx].SetMasterVolume(volume / 100, None)

                self.volume_queue.task_done()
            except queue.Empty:
                continue
            except Exception:
                pass

    def set_app(self, app_idx, app_name):
        """Change the app name for a specific index (e.g., change index 2 from 'brave' to 'chrome')"""
        self.APPS[app_idx] = app_name
        self.app_names_lower[app_idx] = app_name.lower()
        # Force session refresh to pick up new app
        self._refresh_sessions(force=True)

    def get_all_audio_sessions(self):
        """Get list of all active audio session names"""
        sessions = AudioUtilities.GetAllSessions()
        active_apps = set()
        for session in sessions:
            if session.Process and session.State == 1:
                # Extract base name without .exe
                process_name = session.Process.name()
                if process_name.lower().endswith('.exe'):
                    process_name = process_name[:-4]
                active_apps.add(process_name)
        return sorted(list(active_apps))

    def set_volume(self, app_idx, volume):
        """Queue volume change for background processing"""
        self.volume_queue.put((app_idx, volume))

    def read_serial(self):
        """Lê dados do Arduino e retorna dicionário com estados atuais."""
        data = {"volumes": self.last_volumes, "scroll": False}

        while self.arduino.in_waiting > 0:
            line = self.arduino.readline().decode().strip()

            if "," in line:
                # Batched format: "75,50,80"
                volumes = list(map(int, line.split(",")))
                for app_idx, volume in enumerate(volumes):
                    if self.last_volumes[app_idx] != volume:
                        self.last_volumes[app_idx] = volume
                        self.set_volume(app_idx, volume)
                data["volumes"] = self.last_volumes
            elif ":" in line:
                # Legacy format: "0:75" (for backwards compatibility)
                app_idx, volume = map(int, line.split(":"))
                self.last_volumes[app_idx] = volume
                data["volumes"] = self.last_volumes
                self.set_volume(app_idx, volume)
            elif line == "SCROLL":
                pyautogui.press('scrolllock')
                data["scroll"] = True

        return data

    def close(self):
        """Encerra a conexão serial."""
        self.running = False
        self.arduino.close()