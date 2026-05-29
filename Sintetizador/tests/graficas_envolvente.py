import numpy as np
import matplotlib.pyplot as plt
from audio.envolvente import GeneradorEnvolvente

sample_rate = 44100
duracion = 1.5

parametros = {
    "attack": 0.2,
    "decay": 0.3,
    "sustain": 0.6,
    "release": 0.4,
    "sample_rate": sample_rate
}

gate = GeneradorEnvolvente(tipo="gate", **parametros).generar(duracion)
ad = GeneradorEnvolvente(tipo="ad", **parametros).generar(duracion)
adsr = GeneradorEnvolvente(tipo="adsr", **parametros).generar(duracion)

t = np.arange(len(gate)) / sample_rate

plt.figure(figsize=(10, 5))

plt.plot(t, gate, label="Gate")
plt.plot(t, ad, label="AD")
plt.plot(t, adsr, label="ADSR")

plt.title("Comparación entre envolventes Gate, AD y ADSR")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud normalizada")
plt.ylim(-0.05, 1.1)
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.show()