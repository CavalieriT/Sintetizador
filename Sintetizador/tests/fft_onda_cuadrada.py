import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


fs = 44100
duracion = 0.02
frecuencia = 440

# tiempo
t = np.linspace(0, duracion, int(fs * duracion), endpoint=False)

# generar onda cuadrada
onda = signal.square(2 * np.pi * frecuencia * t)

# FFT
fft = np.fft.rfft(onda)
frecuencias = np.fft.rfftfreq(len(onda), 1/fs)

magnitud = np.abs(fft)

plt.figure(figsize=(10, 5))

plt.plot(frecuencias, magnitud)

plt.title("FFT de una onda cuadrada")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Magnitud")

plt.xlim(0, 5000)

plt.grid(True)
plt.tight_layout()

plt.show()