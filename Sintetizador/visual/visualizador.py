import matplotlib.pyplot as plt
import numpy as np
from audio.oscilador import Oscilador

def visualizar_onda(onda, sample_rate=44100, titulo="Forma de onda"):
    """
    Muestra la forma de onda en una ventana de Matplotlib.
    """
    tiempo = np.arange(len(onda)) / sample_rate
    plt.figure(figsize=(10, 4))
    plt.plot(tiempo, onda)
    plt.title(titulo)
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
