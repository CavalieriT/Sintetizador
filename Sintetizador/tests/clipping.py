import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 0.01, 1000)

senal = np.sin(2 * np.pi * 440 * t)

ganancia = 3.0

senal_clip = np.clip(ganancia * senal, -1, 1)

plt.figure(figsize=(10,5))

plt.plot(t, senal, label="Original")
plt.plot(t, senal_clip, label="Con clipping")

plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")

plt.title("Efecto del clipping sobre una señal sinusoidal")

plt.legend()
plt.grid(True)

plt.show()
