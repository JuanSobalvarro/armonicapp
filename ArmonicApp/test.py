import tkinter as tk
from tkinter import ttk
import DFT
import numpy as np
import matplotlib.pyplot as plt

root = tk.Tk()

root.geometry('1000x600')



frame0 = ttk.Frame(root)
frame1 = ttk.Frame(root)
frame0.pack(side='left')
frame1.pack(side='right')


rate = 22000

signal = DFT.record(rate)
N = len(signal)

# aplicar la transformada de Fourier discreta (DFT)
dft = np.fft.fft(signal)

# obtener la magnitud de la DFT
mag = np.abs(dft)

# obtener el eje de frecuencia
freq = np.fft.fftfreq(N, d=1/rate)

# graficar la magnitud en función de la frecuencia
plt.plot(freq[:N//2], mag[:N//2] /1000)
plt.xlim((0,2000))
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Magnitud')
plt.show()


root.mainloop()
