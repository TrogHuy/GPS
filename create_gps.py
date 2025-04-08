import tkinter as tk
from tkinter import ttk
import threading
import time
import json
import random
from datetime import datetime

# Constants
STEP_SIZE = 0.0001
DEVICE_ID = "mock_tracker_01"
SLEEP_INTERVAL = 1  # seconds
PRESET_FILE = "preset_path.txt"

# Load preset path from file
def load_preset_path():
    path = []
    try:
        with open(PRESET_FILE, "r") as file:
            for line in file:
                lat_str, lon_str = line.strip().split(",")
                path.append((float(lat_str), float(lon_str)))
    except Exception as e:
        print(f"Error loading preset path: {e}")
    return path

class GPSSimulator:
    def __init__(self, ui_callback):
        self.running = False
        self.mode = "Random Walk"
        self.lat = 12.9351
        self.lon = 77.6142
        self.index = 0
        self.thread = None
        self.ui_callback = ui_callback
        self.preset_path = load_preset_path()

    def start(self, mode):
        self.mode = mode
        self.running = True
        self.index = 0
        self.thread = threading.Thread(target=self.simulate)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.running = False

    def simulate(self):
        while self.running:
            if self.mode == "Random Walk":
                self.lat += random.uniform(-STEP_SIZE, STEP_SIZE)
                self.lon += random.uniform(-STEP_SIZE, STEP_SIZE)
            elif self.mode == "Preset Path":
                if not self.preset_path:
                    continue
                if self.index >= len(self.preset_path):
                    self.index = 0
                self.lat, self.lon = self.preset_path[self.index]
                self.index += 1

            gps_data = {
                "device_id": DEVICE_ID,
                "latitude": round(self.lat, 6),
                "longitude": round(self.lon, 6),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }

            self.ui_callback(gps_data)
            time.sleep(SLEEP_INTERVAL)

class GPSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GPS Data Simulator")

        self.simulator = GPSSimulator(self.update_display)

        self.mode_var = tk.StringVar(value="Random Walk")

        # UI Components
        ttk.Label(root, text="Mode:").grid(row=0, column=0, padx=5, pady=5)
        self.mode_menu = ttk.Combobox(root, textvariable=self.mode_var, values=["Random Walk", "Preset Path"], state="readonly")
        self.mode_menu.grid(row=0, column=1, padx=5, pady=5)

        self.start_button = ttk.Button(root, text="Start", command=self.start_simulation)
        self.start_button.grid(row=1, column=0, padx=5, pady=10)

        self.stop_button = ttk.Button(root, text="Stop", command=self.stop_simulation)
        self.stop_button.grid(row=1, column=1, padx=5, pady=10)

        self.clear_button = ttk.Button(root, text="Clear", command=self.clear_output)
        self.clear_button.grid(row=1, column=2, padx=5, pady=10)

        self.output = tk.Text(root, height=15, width=60, state="disabled")
        self.output.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    def start_simulation(self):
        self.simulator.start(self.mode_var.get())

    def stop_simulation(self):
        self.simulator.stop()

    def clear_output(self):
        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.config(state="disabled")

    def update_display(self, data):
        self.output.config(state="normal")
        self.output.insert(tk.END, json.dumps(data) + "\n")
        self.output.see(tk.END)
        self.output.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = GPSApp(root)
    root.mainloop()