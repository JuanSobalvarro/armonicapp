import math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import pyaudio
import keyboard as kb
import time

def DFT(signal):
    """
    Calcular la transformada discreta de fourier
    Entrante la signal, array numpy y devuelve el valor complejo de la entrada
    """
    N = len(signal) #limite superior
    n = np.arange(N) #indices de la se;al
    k = n.reshape((N, 1)) # vector con los índices de la DFT
    e = np.exp(-2j * np.pi * k * n / N) # matriz de exponenciales complejas
    dft_signal = np.dot(e, signal) # producto punto entre la matriz y la señal

    return dft_signal



def signal_graph(sample_rate, parent1):
    """
    Hace una grafica en tiempo real de la captura de audio. Y devuelve un np array
    con toda la data recolectada

    parent es donde sera insertado el canva
    """
    chunk_size = 1024
    aformat = pyaudio.paFloat32
    channels = 1

    audio_data = np.zeros(chunk_size * 10)

    full_data = []

    p = pyaudio.PyAudio()

    stream = p.open(format= aformat, channels= channels, rate= sample_rate, input=True, 
                    frames_per_buffer= chunk_size)

    fig = plt.Figure()
    ax = fig.add_subplot(111)
    line, = ax.plot(audio_data)

    """
    dft_fig = plt.Figure()
    dft_ax = dft_fig.add_subplot(111)
    dft_line, = dft_ax.plot([])
    """
    
    


    canvas = FigureCanvasTkAgg(fig, master=parent1)
    canvas.get_tk_widget().pack()
    
    """
    dft_canvas = FigureCanvasTkAgg(dft_fig, master=parent2)
    dft_canvas.get_tk_widget().pack()
    """

    def update_plot():
        #print("update")
        #update input graph
        line.set_ydata(audio_data)
        canvas.draw()


        """
        #update dft graph
        dft = DFT(audio_data)
        #N es 10240
        mag = np.abs(dft)
        freq = np.fft.fftfreq(10240, d=1/sample_rate)

        dft_line.set_xdata(freq[:10240//2])
        dft_line.set_ydata(mag[:10240//2] / 1000)
        dft_canvas.draw()
        """

        parent1.after(10, update_plot)
        #parent2.after(10, update_plot)

    def collect_audio():
        nonlocal audio_data
        nonlocal full_data
        nonlocal stream
        nonlocal p


        audio_chunk = np.frombuffer(stream.read(chunk_size), dtype=np.float32)

        audio_data = np.roll(audio_data, -chunk_size)
        audio_data[-chunk_size:] = audio_chunk


        full_data.append(audio_data)

        if(kb.is_pressed('Escape')):
            plt.close()
            return

        parent1.after(10, collect_audio)

    parent1.after(10, collect_audio)
    parent1.after(10, update_plot)

    parent1.mainloop()

    stream.stop_stream()
    stream.close()
    p.terminate()

    return np.array(full_data)

def record(sample_rate):   
    chunk_size = 1024
    aformat = pyaudio.paFloat32
    channels = 1

    audio_data = []
    

    p = pyaudio.PyAudio()

    stream = p.open(format= aformat, channels= channels, rate= sample_rate, input=True, 
                    frames_per_buffer= chunk_size)

    print('Inicia grabacion')
    
    i = 0
    while(True):
        audio_chunk = np.frombuffer(stream.read(chunk_size), dtype=np.float32)
        audio_data[i*chunk_size:(i+1)*chunk_size] = audio_chunk
        
        if(kb.is_pressed('Escape')):
            break
        

        i += 1

    print('Termina grabacion')
    return audio_data




"""
rate = 22000

signal = signal_graph(rate)
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
"""
