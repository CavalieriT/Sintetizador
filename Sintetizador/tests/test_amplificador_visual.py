import numpy as np
import matplotlib.pyplot as plt

from audio.amplificador import Mezclador, Amplificador


fs = 44100
duracion = 0.01
t = np.linspace(0, duracion, int(fs * duracion), endpoint=False)

senal1 = 0.5 * np.sin(2 * np.pi * 440 * t)
senal2 = 0.5 * np.sin(2 * np.pi * 880 * t)


def dibujar_limites():
    plt.axhline(1.0, color="black", linestyle="--", linewidth=1, alpha=0.7)
    plt.axhline(-1.0, color="black", linestyle="--", linewidth=1, alpha=0.7)


def graficar(numero, titulo, entrada, resultado, color_resultado="red"):
    plt.subplot(numero)
    plt.plot(t, entrada, label="Entrada", color="gray", alpha=0.65, linewidth=1.8)
    plt.plot(t, resultado, label="Resultado", color=color_resultado, linewidth=2)
    dibujar_limites()
    plt.title(titulo, fontsize=11)
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    plt.grid(True)
    plt.legend(fontsize=8, loc="upper right")


# casos del mezclador

mezclador_equilibrado = Mezclador(nivel_osc1=1.0, nivel_osc2=1.0)
mezcla_equilibrada = mezclador_equilibrado.mezclar(senal1, senal2)

mezclador_osc1_domina = Mezclador(nivel_osc1=1.0, nivel_osc2=0.2)
mezcla_osc1_domina = mezclador_osc1_domina.mezclar(senal1, senal2)

mezclador_osc2_domina = Mezclador(nivel_osc1=0.2, nivel_osc2=1.0)
mezcla_osc2_domina = mezclador_osc2_domina.mezclar(senal1, senal2)

mezclador_solo_osc1 = Mezclador(nivel_osc1=1.0, nivel_osc2=0.0)
mezcla_solo_osc1 = mezclador_solo_osc1.mezclar(senal1, senal2)

mezclador_solo_osc2 = Mezclador(nivel_osc1=0.0, nivel_osc2=1.0)
mezcla_solo_osc2 = mezclador_solo_osc2.mezclar(senal1, senal2)


plt.figure(figsize=(14, 12))

graficar(
    321,
    "1. Mezcla equilibrada",
    senal1,
    mezcla_equilibrada,
    "orange"
)

graficar(
    322,
    "2. Mezcla: Oscilador 1 domina",
    senal1,
    mezcla_osc1_domina,
    "orange"
)

graficar(
    323,
    "3. Mezcla: Oscilador 2 domina",
    senal2,
    mezcla_osc2_domina,
    "orange"
)

graficar(
    324,
    "4. Solo Oscilador 1",
    senal1,
    mezcla_solo_osc1,
    "orange"
)

graficar(
    325,
    "5. Solo Oscilador 2",
    senal2,
    mezcla_solo_osc2,
    "orange"
)

plt.suptitle(
    "Prueba visual del Mezclador",
    fontsize=16,
    fontweight="bold",
    y=0.98
)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.subplots_adjust(hspace=0.45)


# casos del amplificador

mezcla_base = mezcla_equilibrada

amp_limpio = Amplificador(
    ganancia=1.5,
    master=0.8,
    normalizar=False,
    saturacion=False
)
senal_amp_limpia = amp_limpio.amplificar(mezcla_base)

amp_fuerte = Amplificador(
    ganancia=3.0,
    master=1.0,
    normalizar=False,
    saturacion=False
)
senal_amp_fuerte = amp_fuerte.amplificar(mezcla_base)

amp_normalizado = Amplificador(
    ganancia=3.0,
    master=0.8,
    normalizar=True,
    saturacion=False
)
senal_amp_normalizada = amp_normalizado.amplificar(mezcla_base)

amp_saturado = Amplificador(
    ganancia=5.0,
    master=1.0,
    normalizar=False,
    saturacion=True
)
senal_amp_saturada = amp_saturado.amplificar(mezcla_base)

amp_master_bajo = Amplificador(
    ganancia=2.0,
    master=0.3,
    normalizar=True,
    saturacion=False
)
senal_master_bajo = amp_master_bajo.amplificar(mezcla_base)


plt.figure(figsize=(14, 12))

graficar(
    321,
    "1. Amplificación limpia",
    mezcla_base,
    senal_amp_limpia,
    "red"
)

graficar(
    322,
    "2. Amplificación fuerte sin normalizar",
    mezcla_base,
    senal_amp_fuerte,
    "red"
)

graficar(
    323,
    "3. Amplificación fuerte normalizada",
    mezcla_base,
    senal_amp_normalizada,
    "red"
)

graficar(
    324,
    "4. Saturación suave",
    mezcla_base,
    senal_amp_saturada,
    "red"
)

graficar(
    325,
    "5. Master bajo",
    mezcla_base,
    senal_master_bajo,
    "red"
)

plt.suptitle(
    "Prueba visual del Amplificador",
    fontsize=16,
    fontweight="bold",
    y=0.98
)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.subplots_adjust(hspace=0.45)

plt.show()
