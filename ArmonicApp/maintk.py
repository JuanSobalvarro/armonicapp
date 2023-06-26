import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import webbrowser
import pyaudio
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import keyboard as kb
    
global audioDeviceID, updateAudioStream, up, bot, audioDevice

audioDeviceID = 0
updateAudioStream = False
audioDevice = ""


class App(tk.Tk):
    
    def __init__(self):
        super().__init__()

        self.w = 1020
        self.h = 600

        self.title('ArmonicApp')
        self.geometry(f'{self.w}x{self.h}')
        self.resizable(1,1)

        BarMenu(self)

        global up, bot

        bot = BottFrame(self, width=self.w, height=self.h/2, borderwidth=10, relief=tk.RIDGE)
        up = UpFrame(self, width=self.w, height=self.h/2, borderwidth=10, relief=tk.RIDGE)
        
        up.pack(side="top")
        bot.pack(side="bottom")
        
        

        self.mainloop()

class BarMenu(tk.Menu):
    def __init__(self, parent):
        super().__init__()
        
        parent.config(menu=self)
        
        #file sub menu
        file = tk.Menu(self, tearoff=False)
        self.add_cascade(label='File', menu=file)

        file.add_command(label='Help', command= lambda: webbrowser.open_new("https://github.com/JuanSobalvarro/"))
        file.add_separator()
        file.add_command(label='Exit', command= parent.destroy)

        #config sub menu
        config = tk.Menu(self, tearoff=False)
        self.add_cascade(label='Configuration', menu=config)

        config.add_command(label='Scalate configuration', command= lambda: print('scalate config'))

        audiodevmen = tk.Menu(self, tearoff=False)
        
        self.p = pyaudio.PyAudio()
        info = self.p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')

        print(numdevices)

        for i in range(0, int(numdevices/2)):
            if (self.p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                name = "Id " + str(i) + self.p.get_device_info_by_host_api_device_index(1, i).get('name')
                audiodevmen.add_command(label=name, command= lambda: self.selectAudioDevice(i))


        config.add_cascade(label='Audio Devices', menu=audiodevmen)

    def selectAudioDevice(self, ID):
        global audioDevice, updateAudioStream, audioDeviceID


        audioDevice = self.p.get_device_info_by_host_api_device_index(1, ID).get('name')
        updateAudioStream = True
        audioDeviceID = ID-1


class UpFrame(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.pack(side="top", expand=True, fill="both")
        
        #botones uwu
        self.b0 = ttk.Button(self, width=30, text="Initialize audio and transformation", command= lambda: bot.signal_graph(22000))
        self.b0.grid(column=0, row=0)

        #self.b1 = ttk.Button(self, width=30, text="uwu2", command= lambda: bot.notes_graph(22000))
        #self.b1.grid(column=0, row=1)

        self.label0 = ttk.Label(self, text="Escalado de X")
        self.label1 = ttk.Label(self, text="Escalado de Y")

        self.label0.grid(column=0, row=1)
        self.label1.grid(column=0, row=2)

        #reescalador de grafica frecuencias

        xlim = tk.IntVar()
        ylim = tk.IntVar()

        self.sliderx = ttk.Scale(self, from_=20, to=20000, variable=xlim)
        self.slidery = ttk.Scale(self, from_=0, to=100, variable=ylim)

        self.sliderx.set(10000)
        self.slidery.set(50)

        self.sliderx.grid(column=1, row=1)
        self.slidery.grid(column=1, row=2)
        
        self.label2 = ttk.Label(self, text=self.sliderx.get())
        self.label3 = ttk.Label(self, text=self.slidery.get())

        self.label2.grid(column=2, row=1)
        self.label3.grid(column=2, row=2)

        self.label4 = ttk.Label(self, text="Audio device selected:")
        self.label4.grid(column=3, row=0)

        self.label5 = ttk.Label(self, textvariable=audioDevice)
        self.label5.grid(column=3, row=1)


     

class BottFrame(ttk.Frame):

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.dft_fig = plt.Figure()
        self.dft_ax = self.dft_fig.add_subplot(111)

        self.dft_ylim = 100
        self.dft_xlim = 10000 

        self.pack(side="bottom", expand=True, fill="both")

        self.f0 = tk.Frame(self, relief='raised')
        self.f0.pack(side="left", expand=False, fill="none")
        

        self.f1 = tk.Frame(self, relief='raised')
        self.f1.pack(side="right", expand=False, fill="none")
    

    def signal_graph(self, sample_rate):
        #show signal graph donde se mostrara la signal entrante y la DFT con las frecuencias
        """
        Hace una grafica en tiempo real de la captura de audio. Y devuelve un np array
        con toda la data recolectada

        parent es donde sera insertado el canva
        """
        
        i = 0

        cw = 500
        ch = 200

        chunk_size = 1024
        aformat = pyaudio.paFloat32
        channels = 1

        audio_data = np.zeros(chunk_size * 5) 

        
        #self.full_data = []

        p = pyaudio.PyAudio()

        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')

        for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

        stream = p.open(format= aformat, channels= channels, rate= sample_rate, input=True, 
                        frames_per_buffer= chunk_size, input_device_index=audioDeviceID)

        fig = plt.Figure()
        ax = fig.add_subplot(111)
        line, = ax.plot(audio_data)
        
        
        dft_line, = self.dft_ax.plot(np.fft.fft(audio_data), color='#149166')
        
        
        

        canvas = FigureCanvasTkAgg(fig, master=self.f0)
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().config(width=cw, height=ch)

        dft_canvas = FigureCanvasTkAgg(self.dft_fig, master=self.f1)
        dft_canvas.get_tk_widget().pack()
        dft_canvas.get_tk_widget().config(width=520)
        

        def update_plot():
            #print("update")
            #update input graph

            self.dft_ax.set_xlim([0, up.sliderx.get()])
            self.dft_ax.set_ylim([0, up.slidery.get()])

            up.label2.configure(text=int(up.sliderx.get()))
            up.label3.configure(text=int(up.slidery.get()))

            #calcular la dft
            signal = audio_data

            rate = 22000
            N = len(signal)

            # aplicar la transformada de Fourier discreta (DFT)
            dft = np.fft.fft(signal)

            # obtener la magnitud de la DFT
            mag = np.abs(dft)

            

            # obtener el eje de frecuencia
            freq = np.fft.fftfreq(N, d=1/rate)


            line.set_ydata(audio_data)
             
            dft_line.set_ydata(mag[:N//2])
            dft_line.set_xdata(freq[:N//2])
            canvas.draw()
            dft_canvas.draw()

            self.f0.after(5, update_plot)
        
        
        def collect_audio():
            nonlocal audio_data
            nonlocal stream
            nonlocal p
            nonlocal i
            nonlocal sample_rate
            nonlocal chunk_size
            nonlocal channels

            global updateAudioStream

            #print('collecting')

            if(updateAudioStream):
                devinfo = p.get_device_info_by_index(audioDeviceID)

                print(devinfo['maxInputChannels'])
                channels = devinfo['maxInputChannels']
                chunk_size = 1024

                stream.close()
                p.terminate()

                p = pyaudio.PyAudio()

                stream = p.open(format= aformat, channels=channels, rate= sample_rate, input=True, 
                    frames_per_buffer= chunk_size, input_device_index=audioDeviceID)

                up.label5.config(textvariable=devinfo['name'])
                
                updateAudioStream = False

                
            audio_chunk = np.frombuffer(stream.read(chunk_size), dtype=np.float32)
            audio_data = np.roll(audio_data, -chunk_size)
            audio_data[-2048:] = audio_chunk
            #en debug derecha es chunksize e izquierda es el audio chunk

            self.f0.after(5, collect_audio)

        self.f0.after(5, collect_audio)
        
        self.f0.after(5, update_plot)

        self.f0.mainloop()
    
App()