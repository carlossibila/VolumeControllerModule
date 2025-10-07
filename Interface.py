import tkinter as tk
from tkinter import ttk
from Handler import VolumeController
import threading
import json
import os

class AppInterface:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.config_file = "audio_module_config.json"

        # Load saved config
        self._load_config()

        # Pre-cache app names list to avoid repeated conversions
        self.app_names = list(self.controller.APPS.values())
        self.setup_ui()
        self.update_interface()

    def _load_config(self):
        """Load saved third node app selection"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    if 'node3_app' in config:
                        self.controller.set_app(2, config['node3_app'])
            except Exception:
                pass

    def _save_config(self):
        """Save third node app selection"""
        try:
            config = {'node3_app': self.controller.APPS[2]}
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
        except Exception:
            pass

    def setup_ui(self):
        self.root.title("Volume Module")
        self.root.geometry("350x300")

        # Volumes (%) - First two are fixed
        self.volume_labels = []
        for i, app in enumerate(self.app_names[:2]):
            label = ttk.Label(self.root, text=f"{app}: 0%")
            label.pack(pady=5)
            self.volume_labels.append(label)

        # Third node with dropdown
        node3_frame = ttk.Frame(self.root)
        node3_frame.pack(pady=5)

        self.volume_label_3 = ttk.Label(node3_frame, text=f"{self.app_names[2]}: 0%")
        self.volume_label_3.pack(side=tk.LEFT, padx=5)
        self.volume_labels.append(self.volume_label_3)

        # Dropdown for node 3
        self.dropdown_var = tk.StringVar(value=self.controller.APPS[2])
        self.app_dropdown = ttk.Combobox(
            node3_frame,
            textvariable=self.dropdown_var,
            width=15,
            state='readonly'
        )
        self.app_dropdown.pack(side=tk.LEFT, padx=5)
        self.app_dropdown.bind('<<ComboboxSelected>>', self._on_app_changed)

        # Refresh button for dropdown
        ttk.Button(node3_frame, text="↻", width=3, command=self._refresh_dropdown).pack(side=tk.LEFT)

        # Initial dropdown population
        self._refresh_dropdown()

        # Estado do Scroll
        self.scroll_label = ttk.Label(self.root, text="Click: False")
        self.scroll_label.pack(pady=10)

        # Botão de fechar
        ttk.Button(self.root, text="Fechar", command=self.close).pack()

    def _refresh_dropdown(self):
        """Refresh available audio sessions in dropdown"""
        available_apps = self.controller.get_all_audio_sessions()
        self.app_dropdown['values'] = available_apps
        # Keep current selection if it's still available
        if self.controller.APPS[2] not in available_apps and available_apps:
            self.dropdown_var.set(available_apps[0])
            self._on_app_changed()

    def _on_app_changed(self, event=None):
        """Handle dropdown selection change"""
        new_app = self.dropdown_var.get()
        if new_app:
            self.controller.set_app(2, new_app)
            self.app_names[2] = new_app
            self._save_config()

    def update_interface(self):
        if self.controller.running:
            data = self.controller.read_serial()

            # Atualiza volumes
            for i, volume in enumerate(data["volumes"]):
                if volume != -1:  # Ignora cache inválido
                    self.volume_labels[i].config(text=f"{self.app_names[i]}: {volume}%")

            # Atualiza scroll
            if data["scroll"]:
                self.scroll_label.config(text="Click: True")
                self.root.after(1000, lambda: self.scroll_label.config(text="Click: False"))

            self.root.after(50, self.update_interface)

    def close(self):
        self.controller.close()
        self.root.destroy()

def start_interface(controller):
    root = tk.Tk()
    AppInterface(root, controller)
    root.mainloop()

if __name__ == "__main__":
    controller = VolumeController()
    # Thread para não bloquear a interface
    serial_thread = threading.Thread(target=controller.read_serial, daemon=True)
    serial_thread.start()
    start_interface(controller)