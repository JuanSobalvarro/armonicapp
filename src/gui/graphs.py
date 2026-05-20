import tkinter as tk
from tkinter import ttk
import numpy as np
import queue
import sounddevice as sd
import threading
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.processing.dft import compute_dft


class Graphs(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.sample_rate = 44100
        self.chunk_size = 1024
        self.buffer_size = self.chunk_size * 8

        self.audio_buffer = np.zeros(self.buffer_size, dtype=np.float32)

        self.audio_queue = queue.Queue()

        self.stream = None
        self._worker_thread = None
        self._worker_stop = threading.Event()
        self._plot_update_job = None
        self.latest_dft = np.zeros(self.buffer_size // 2 + 1)
        self.latest_freqs = np.zeros(self.buffer_size // 2 + 1)
        self.freq_limit = self.sample_rate // 2
        self.y_limit = 100

        # Matplotlib figure for waveform + DFT (two rows)
        self.fig = Figure(figsize=(6, 6))
        self.ax = self.fig.add_subplot(211)
        self.line, = self.ax.plot(self.audio_buffer)
        self.ax.set_ylim(-1, 1)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # DFT subplot (below waveform)
        self.dft_ax = self.fig.add_subplot(212)
        self.dft_line, = self.dft_ax.plot(self.latest_dft, color='#149166')
        self.dft_ax.set_ylim(0, self.y_limit)
        self.dft_ax.set_xlim(0, self.freq_limit)

    def signal_graph(self, sample_rate: int):
        if self.stream is not None:
            return

        self.sample_rate = sample_rate

        try:
            self.stream = sd.InputStream(samplerate=self.sample_rate,
                                         channels=1,
                                         callback=self._sd_callback,
                                         blocksize=self.chunk_size)
            self.stream.start()
        except Exception as e:
            print("Failed to start InputStream:", e)
            self.stream = None
            return

        # start worker thread for DFT processing
        self._worker_stop.clear()
        self._worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker_thread.start()

        # start the GUI update loop
        if self._plot_update_job is None:
            self._plot_update_job = self.after(30, self._update_plot)

    def _sd_callback(self, indata, frames, time, status):
        if status:
            print(status)
        # put a copy into the queue
        try:
            self.audio_queue.put(indata[:, 0].copy(), block=False)
        except queue.Full:
            pass

    def _worker_loop(self):
        # runs in background thread: consumes audio_queue, updates buffer and computes DFT
        window = np.hanning(self.buffer_size)
        while not self._worker_stop.is_set():
            try:
                chunk = self.audio_queue.get(timeout=0.1)
            except Exception:
                continue

            n = len(chunk)
            if n >= self.buffer_size:
                self.audio_buffer = chunk[-self.buffer_size:].copy()
            else:
                self.audio_buffer = np.roll(self.audio_buffer, -n)
                self.audio_buffer[-n:] = chunk

            # compute DFT on a copy to avoid races
            try:
                sig = self.audio_buffer.copy() * window
                freqs, mags = compute_dft(sig, self.sample_rate)
                self.latest_freqs = freqs
                self.latest_dft = mags
            except Exception as e:
                print("DFT error:", e)

    def _update_plot(self):
        self.line.set_ydata(self.audio_buffer)
        self.ax.set_xlim(0, len(self.audio_buffer))

        if self.latest_dft is not None and len(self.latest_dft) > 0:
            self.dft_line.set_data(self.latest_freqs, self.latest_dft)

        self.canvas.draw_idle()

        self._plot_update_job = self.after(30, self._update_plot)

    def stop(self):
        if self.stream is not None:
            try:
                self.stream.stop()
                self.stream.close()
            except Exception:
                pass
            self.stream = None
        # stop worker
        if self._worker_thread is not None:
            self._worker_stop.set()
            self._worker_thread.join(timeout=1.0)
            self._worker_thread = None
        if self._plot_update_job is not None:
            self.after_cancel(self._plot_update_job)
            self._plot_update_job = None

    def update_freq_limit(self, value: int):
        self.freq_limit = max(1, int(value))
        self.dft_ax.set_xlim(0, self.freq_limit)
        self.canvas.draw_idle()

    def update_y_limit(self, value: int):
        self.y_limit = max(1, int(value))
        self.dft_ax.set_ylim(0, self.y_limit)
        self.canvas.draw_idle()
