import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 0.01, 1000)

senal = 2 * np.sin(2 * np.pi * 440 * t)

senal_tanh = np.tanh(senal)

plt.figure(figsize=(10,5))

plt.plot(t, senal, label="Original")
plt.plot(t, senal_tanh, label="Con saturación tanh")

plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")

plt.title("Saturación suave mediante función tanh")

plt.legend()
plt.grid(True)

plt.show()
