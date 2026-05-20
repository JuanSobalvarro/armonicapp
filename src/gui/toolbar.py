import tkinter as tk
from tkinter import ttk
import webbrowser
import sounddevice as sd
from src.audio import AudioManager


class Toolbar(tk.Menu):
    def __init__(self, parent, audioManager: AudioManager):
        super().__init__(parent)

        self.audioManager = audioManager
        self.device_selected_callback = None

        parent.config(menu=self)

        self.file_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Help", command=self.open_help)

        self.config_menu = tk.Menu(self, tearoff=False)
        self.audio_device_menu = tk.Menu(self, tearoff=False)

        self.add_cascade(label="Config", menu=self.config_menu)
        self.config_menu.add_cascade(label="Audio Device", menu=self.audio_device_menu)

        devices = self.audioManager.get_audio_devices()
        for device in devices:
            self.audio_device_menu.add_command(label=device, command=lambda d=device: self.select_device(d))

    def select_device(self, device_name):
        for item in self.audioManager.get_audio_devices():
            if item == device_name:
                self.audioManager.select_audio_device(device_name)

                if self.device_selected_callback is not None:
                    self.device_selected_callback(device_name)

                break

    def set_device_selected_callback(self, callback):
        self.device_selected_callback = callback

    @staticmethod
    def open_help():
        webbrowser.open_new("https://github.com/JuanSobalvarro/")

    