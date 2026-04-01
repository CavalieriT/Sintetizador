import numpy as np
import matplotlib.pyplot as plt
from filtros import Filtro

fs = 44100
duracion = 0.01
t = np.linspace(0, duracion, int(fs*duracion), endpoint=False)

signal = (
    np.sin(2*np.pi*200*t) +
    np.sin(2*np.pi*800*t) +
    np.sin(2*np.pi*1200*t) +
    np.sin(2*np.pi*3000*t)
)

lowpass = Filtro(tipo="lowpass", cutoff=800, sample_rate=fs)
highpass = Filtro(tipo="highpass", cutoff=800, sample_rate=fs)
bandpass = Filtro(tipo="bandpass", cutoff=1000, bandwidth=600, sample_rate=fs)

señal_low = lowpass.aplicar(signal)
señal_high = highpass.aplicar(signal)
señal_band = bandpass.aplicar(signal)

def dibujar(original, filtrada, titulo):
    plt.figure(figsize=(8, 5))
    plt.plot(t, original, label="original")
    plt.plot(t, filtrada, label="filtered")
    plt.title(titulo)
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

dibujar(signal, señal_low, "Test Low-pass")
dibujar(signal, señal_high, "Test High-pass")
dibujar(signal, señal_band, "Test Band-pass")

plt.show()