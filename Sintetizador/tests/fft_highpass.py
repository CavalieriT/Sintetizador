import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

from audio.filtros import Filtro


fs = 44100
duracion = 0.1
frecuencia = 440
cutoff = 1000

t = np.linspace(0, duracion, int(fs * duracion), endpoint=False)

onda = signal.square(2 * np.pi * frecuencia * t)

filtro = Filtro(
    tipo='highpass',
    cutoff=cutoff,
    sample_rate=fs
)

onda_filtrada = filtro.aplicar(onda)

# FFT
fft_original = np.fft.rfft(onda)
fft_filtrada = np.fft.rfft(onda_filtrada)
freqs = np.fft.rfftfreq(len(onda), 1 / fs)

mag_original = np.abs(fft_original)
mag_filtrada = np.abs(fft_filtrada)

# usar el mismo factor de normalización para ambas magnitudes
maximo = max(
    np.max(mag_original),
    np.max(mag_filtrada)
)

mag_original /= maximo
mag_filtrada /= maximo

plt.figure(figsize=(10, 6))

plt.plot(freqs, mag_original, label="Original", alpha=0.7)
plt.plot(freqs, mag_filtrada, label="Filtrada (highpass)", linewidth=2)

plt.xlim(0, 5000)
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Magnitud normalizada")
plt.title("FFT antes y después del filtro paso alto")

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig("fft_highpass.png", dpi=300, bbox_inches="tight")
plt.show()