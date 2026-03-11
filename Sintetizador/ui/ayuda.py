import tkinter as tk
from tkinter import ttk

TEXTO_AYUDA = """
Bienvenido al Sintetizador Didáctico

1) ¿Qué hace cada cosa?
- Frecuencia: controla qué tan agudo o grave es el sonido (tono).
- Amplitud: controla el volumen del oscilador.
- Forma de onda: cambia el "color" del sonido:
  • Seno: sonido suave y limpio (como un silbido).
  • Cuadrada: sonido más hueco y rico (como un clarinete).
  • Triangular: sonido intermedio (suave pero con cuerpo).
  • Sierra: sonido brillante y denso (como un violín).
- Unison: genera varias copias del mismo sonido, ligeramente desafinadas, para crear grosor.
- Detune: cuánto se desafinan esas copias (valores pequeños = más suave, valores grandes = más separado).

2) Interacciones entre osciladores
- Ninguna: suma los dos osciladores (suenan juntos).
- FM: el oscilador 2 modula la frecuencia del 1, creando nuevos timbres.
  • Índice bajo = armónicos sutiles; índice alto = sonido metálico tipo campana.
- Ring Mod: multiplica ambos sonidos, creando efectos metálicos o robóticos.
- Sync: el oscilador 2 reinicia el 1, generando un sonido más brillante y rico en armónicos.

3) ¿Cómo empezar?
- Elige una forma de onda para cada oscilador.
- Ajusta la frecuencia para cambiar el tono.
- Si quieres sonido más "gordo", sube Unison y añade un poco de Detune (5-15 suele funcionar bien).
- Selecciona una interacción (Ninguna/FM/Ring/Sync) y prueba.
- Toca una nota en el teclado o pulsa "Reproducir sonido".
- Observa las gráficas para ver cómo cambia la onda.

4) Presets (sonidos predefinidos)
- Init: punto de partida limpio.
- Unison Lead: sonido ancho ideal para melodías principales.
- FM Bell: sonido de campana usando FM.
- Ring Metal: efecto metálico con modulación en anillo.
- Sync Bright: sonido brillante con sincronización.

Tip: pasa el ratón por los controles para ver ayudas rápidas.
"""

TEXTO_GUIA_INICIO = """
GUÍA: Cómo crear tu primer sonido desde cero

Paso 1: Empieza simple
• Selecciona el preset "Init" para resetear todo.
• Observa las tres gráficas: muestran las ondas del oscilador 1, oscilador 2 y la combinación.

Paso 2: Ajusta el Oscilador 1
• Deja la forma en "sinusoidal" (sonido limpio).
• Mueve el slider de Frecuencia hacia arriba o abajo para cambiar el tono.
• Ajusta Amplitud a 0.8 aproximadamente.
• Deja Unison en 1 y Detune bajado por completo.

Paso 3: Ajusta el Oscilador 2
• Cambia la forma a "cuadrada" (sonido más rico).
• Ajusta la frecuencia para que sea diferente a la del oscilador 1 (prueba con 660 Hz).
• Amplitud a 0.5.
• Unison en 1, Detune bajado por completo.

Paso 4: Selecciona una interacción
• Deja "ninguna" seleccionado (suma simple de ambos osciladores).
• Haz clic en "Reproducir sonido" para escuchar la combinación.
• Observa la gráfica "Onda Combinada" (suma de ambas ondas).

Paso 5: Experimenta con Unison y Detune
• En el oscilador 1, sube Unison a 3 voces.
• Sube Detune un poco
• Reproduce de nuevo → el sonido ahora es más "gordo" y ancho.

Paso 6: Prueba interacciones
• Cambia "ninguna" a "fm".
• Sube un poco el FM index.
• Reproduce → sonido tipo campana.
• Prueba "ring_mod" → sonido metálico.
• Prueba "sync" → sonido brillante.

Paso 7: Usa el teclado
• Haz clic en las teclas del teclado virtual para tocar notas.
• Cada clic reproduce el sonido con la frecuencia de esa nota.
• Combina diferentes configuraciones de osciladores e interacciones para explorar timbres.

Paso 8: Prueba los presets
• Selecciona "Unison Lead" → sonido ancho ideal para melodías.
• Selecciona "FM Bell" → campana con FM.
• Observa qué parámetros cambian y cómo afectan al sonido.

Consejo final:
• No tengas miedo de experimentar: cambia todos los parámetros y observa las gráficas.
• Los tooltips (al pasar el ratón) te dan ayuda rápida en cada control.
• Usa los botones "?" en cada sección para ayuda específica.

¡Diviértete creando sonidos!
"""

def mostrar_ayuda(parent):
    win = tk.Toplevel(parent)
    win.title("Ayuda del sintetizador")
    win.geometry("640x520")
    win.resizable(True, True)

    frm = ttk.Frame(win)
    frm.pack(fill="both", expand=True, padx=10, pady=10)

    txt = tk.Text(frm, wrap="word")
    scr = ttk.Scrollbar(frm, orient="vertical", command=txt.yview)
    txt.configure(yscrollcommand=scr.set)
    txt.insert("1.0", TEXTO_AYUDA)
    txt.configure(state="disabled")

    txt.pack(side="left", fill="both", expand=True)
    scr.pack(side="right", fill="y")

    btn = ttk.Button(win, text="Cerrar", command=win.destroy)
    btn.pack(pady=6)

def mostrar_guia_inicio(parent):
    win = tk.Toplevel(parent)
    win.title("Cómo empezar - Guía paso a paso")
    win.geometry("700x600")
    win.resizable(True, True)

    frm = ttk.Frame(win)
    frm.pack(fill="both", expand=True, padx=10, pady=10)

    txt = tk.Text(frm, wrap="word", font=("Arial", 10))
    scr = ttk.Scrollbar(frm, orient="vertical", command=txt.yview)
    txt.configure(yscrollcommand=scr.set)
    txt.insert("1.0", TEXTO_GUIA_INICIO)
    txt.configure(state="disabled")

    txt.pack(side="left", fill="both", expand=True)
    scr.pack(side="right", fill="y")

    btn = ttk.Button(win, text="Cerrar", command=win.destroy)
    btn.pack(pady=6)