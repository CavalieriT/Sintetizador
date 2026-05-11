#runnear con python -m tests.fft_lowpass
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

from audio.filtros import Filtro

fs = 44100
duracion = 0.1
frecuencia = 440

t = np.linspace(0, duracion, int(fs * duracion), endpoint=False)

# señal original onda cuadrada
onda = signal.square(2 * np.pi * frecuencia * t)

# usando filtro del sintetizador
filtro = Filtro(
    tipo='lowpass',
    cutoff=1000,
    sample_rate=fs
)

onda_filtrada = filtro.aplicar(onda)

#FFT original
fft_original = np.fft.rfft(onda)
freqs = np.fft.rfftfreq(len(onda), 1/fs)

#FFT filtrada
fft_filtrada = np.fft.rfft(onda_filtrada)

#normalización de magnitudes
mag_original = np.abs(fft_original)
mag_filtrada = np.abs(fft_filtrada)

mag_original /= np.max(mag_original)
mag_filtrada /= np.max(mag_filtrada)

plt.figure(figsize=(10, 6))

plt.plot(freqs, mag_original, label="Original")
plt.plot(freqs, mag_filtrada, label="Filtrada (lowpass)")

plt.xlim(0, 5000)

plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Magnitud normalizada")

plt.title("FFT antes y después del filtro paso bajo")

plt.legend()
plt.grid(True)

plt.tight_layout()

plt.savefig(
    "fft_lowpass.png",
    dpi=300,
    bbox_inches='tight'
)

plt.show()