import numpy as np
import matplotlib.pyplot as plt
from audio.envolvente import GeneradorEnvolvente

env = GeneradorEnvolvente(
    tipo="adsr",
    attack=0.1,
    decay=0.2,
    sustain=0.6,
    release=0.3,
    sample_rate=44100
)

duracion = 1.5
envolvente = env.generar(duracion)
t = np.arange(len(envolvente)) / 44100

plt.figure(figsize=(10, 4))
plt.plot(t, envolvente)
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.title("Envolvente ADSR generada")
plt.grid(True)
plt.tight_layout()
plt.show()