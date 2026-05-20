import tkinter as tk
from tkinter import ttk
from src.gui.toolbar import Toolbar
from src.gui.options import Options
from src.gui.graphs import Graphs


class App(tk.Tk):
    def __init__(self, audioManager):
        super().__init__()

        self.audioManager = audioManager

        self.w = 1020
        self.h = 600

        self.title("ArmonicApp")
        self.geometry(f"{self.w}x{self.h}")
        self.resizable(True, True)

        self.setup_ui()

    def setup_ui(self):
        self.toolbar = Toolbar(self, audioManager=self.audioManager)

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.options_frame = ttk.Frame(self.main_frame, width=200)
        self.options_frame.pack(side=tk.LEFT, fill=tk.Y)

        # central content area for graphs
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.graphs = Graphs(self.content_frame)
        self.graphs.pack(fill=tk.BOTH, expand=True)

        self.options = Options(
            self.options_frame,
            start_callback=self.graphs.signal_graph,
            stop_callback=self.graphs.stop,
            update_freq_limit_callback=self.graphs.update_freq_limit,
            update_y_limit_callback=self.graphs.update_y_limit,
        )
        self.options.pack(fill=tk.BOTH, expand=True)

        # keep the selected device label in sync with toolbar selection
        self.toolbar.set_device_selected_callback(self.options.set_selected_device)
        current_device = self.audioManager.get_selected_device()
        if current_device:
            self.options.set_selected_device(current_device)

