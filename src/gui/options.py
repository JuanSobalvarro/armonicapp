import tkinter as tk
from tkinter import ttk
from typing import Callable


class Options(ttk.Frame):
    def __init__(
        self,
        parent,
        start_callback,
        stop_callback: Callable[[], None],
        update_freq_limit_callback: Callable[[int], None],
        update_y_limit_callback: Callable[[int], None],
        **kwargs,
    ):
        super().__init__(parent, **kwargs)

        self.start_callback = start_callback
        self.stop_callback = stop_callback
        self.update_freq_limit_callback = update_freq_limit_callback
        self.update_y_limit_callback = update_y_limit_callback

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.label = ttk.Label(self, text="Options")
        self.label.pack(pady=10)

        self.device_label_title = ttk.Label(self, text="Current device")
        self.device_label_title.pack(pady=(8, 0))

        self.device_name_var = tk.StringVar(value="No device selected")
        self.device_label = ttk.Label(self, textvariable=self.device_name_var, wraplength=180)
        self.device_label.pack(pady=(0, 10))
        
        self.start_button = ttk.Button(self, text="Start", command=self.start)
        self.start_button.pack(pady=5)

        self.stop_button = ttk.Button(self, text="Stop", command=self.stop)
        self.stop_button.pack(pady=5)

        # x (freq) and y (amplitude) sliders for max limit of DFT graph
        self.freq_limit_label = ttk.Label(self, text="Frequency Limit (Hz)")
        self.freq_limit_label.pack(pady=10)
        self.freq_limit_slider = ttk.Scale(self, from_=1000, to=20000, orient=tk.HORIZONTAL, command=self.update_freq_limit)
        self.freq_limit_slider.set(20000)
        self.freq_limit_slider.pack(fill=tk.X, padx=10)

        self.y_limit_label = ttk.Label(self, text="Amplitude Limit")
        self.y_limit_label.pack(pady=10)
        self.y_limit_slider = ttk.Scale(self, from_=10, to=1000, orient=tk.HORIZONTAL, command=self.update_y_limit)
        self.y_limit_slider.set(100)
        self.y_limit_slider.pack(fill=tk.X, padx=10)

    def set_selected_device(self, device_name: str):
        self.device_name_var.set(device_name or "No device selected")

    def update_freq_limit(self, value):
        self.update_freq_limit_callback(int(float(value)))

    def update_y_limit(self, value):
        self.update_y_limit_callback(int(float(value)))

    def start(self):
        self.start_callback(44100)

    def stop(self):
        self.stop_callback()

