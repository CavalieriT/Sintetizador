import tkinter as tk
from tkinter import ttk
from ui.widgets import Knob, Tooltip, crear_labelframe_con_ayuda

def crear_controles_osciladores(parent, freq1, amp1, forma1, unison1, detune1, freq2, amp2, forma2, unison2, detune2, update_callback):
    """
    Crea los controles de los dos osciladores con unison y detune individuales.
    """
    texto_ayuda = """Los osciladores generan ondas de sonido básicas.

• Frecuencia: qué tan agudo (alto) o grave (bajo) suena.
• Amplitud: el volumen del oscilador.
• Forma de onda: el 'color' del sonido:
  - Seno: limpio y suave (como un silbido).
  - Cuadrada: hueco y rico (tipo clarinete).
  - Triangular: intermedio, suave con cuerpo.
  - Sierra: brillante y denso (tipo violín).
• Unison: genera varias copias del sonido ligeramente desafinadas para crear grosor.
• Detune: cuánto se desafinan la frecuencia de esas copias.

Consejo: empieza con 1 voz y sin detune, luego experimenta subiendo unison y detune poco a poco."""
    
    frame, _ = crear_labelframe_con_ayuda(parent, "Controles de Osciladores", texto_ayuda)
    frame.pack(fill="x", pady=4)

    osc1_frame = ttk.LabelFrame(frame, text="Oscilador 1")
    osc1_frame.grid(row=0, column=0, padx=8, pady=6, sticky="nsew")

    osc2_frame = ttk.LabelFrame(frame, text="Oscilador 2")
    osc2_frame.grid(row=0, column=1, padx=8, pady=6, sticky="nsew")

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)

    freq1_label = tk.StringVar(value=f"{freq1.get():.1f} Hz")
    amp1_label = tk.StringVar(value=f"{amp1.get():.2f}")
    freq2_label = tk.StringVar(value=f"{freq2.get():.1f} Hz")
    amp2_label = tk.StringVar(value=f"{amp2.get():.2f}")

    def slider_changed(var, label_var, fmt, val):
        var.set(float(val))
        label_var.set(fmt.format(float(val)))
        update_callback()

    def crear_entry_frecuencia(parent_frame, freq_var, label_var, scale_widget):
        """Crea un Entry editable para introducir frecuencia manualmente."""
        entry = ttk.Entry(parent_frame, textvariable=label_var, width=10, justify='center')
        
        def on_focus_in(e):
            # Al hacer clic, seleccionar solo el número (sin " Hz")
            current = label_var.get()
            if current.endswith(" Hz"):
                label_var.set(current[:-3])
            entry.select_range(0, tk.END)
        
        def on_focus_out(e):
            # Al perder foco, validar y añadir " Hz"
            try:
                val = float(label_var.get())
                val = max(20.0, min(2000.0, val))  # Limitar rango
                freq_var.set(val)
                label_var.set(f"{val:.1f} Hz")
                scale_widget.set(val)
                update_callback()
            except ValueError:
                # Si hay error, restaurar valor anterior
                label_var.set(f"{freq_var.get():.1f} Hz")
        
        def on_return(e):
            entry.master.focus()  # Quitar foco para activar validación
        
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        entry.bind("<Return>", on_return)
        
        return entry

    def crear_entry_amplitud(parent_frame, amp_var, label_var, scale_widget):
        """Crea un Entry editable para introducir amplitud manualmente."""
        entry = ttk.Entry(parent_frame, textvariable=label_var, width=10, justify='center')
        
        def on_focus_in(e):
            # Al hacer clic, seleccionar todo el contenido
            entry.select_range(0, tk.END)
        
        def on_focus_out(e):
            # Al perder foco, validar
            try:
                val = float(label_var.get())
                val = max(0.0, min(1.0, val))  # Limitar rango 0.0-1.0
                amp_var.set(val)
                label_var.set(f"{val:.2f}")
                scale_widget.set(val)
                update_callback()
            except ValueError:
                # Si hay error, restaurar valor anterior
                label_var.set(f"{amp_var.get():.2f}")
        
        def on_return(e):
            entry.master.focus()  # Quitar foco para activar validación
        
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        entry.bind("<Return>", on_return)
        
        return entry

    # Oscilador 1
    ttk.Label(osc1_frame, text="Freq (Hz)").grid(row=0, column=0, pady=(4,0))
    freq1_scale = ttk.Scale(osc1_frame, from_=2000, to=20, orient='vertical',
                            command=lambda v: slider_changed(freq1, freq1_label, "{:.1f} Hz", v))
    freq1_scale.set(freq1.get())
    freq1_scale.grid(row=1, column=0, padx=6, rowspan=3)
    Tooltip(freq1_scale, "Controla qué tan agudo (alto) o grave (bajo) es el sonido.")
    freq1_entry = crear_entry_frecuencia(osc1_frame, freq1, freq1_label, freq1_scale)
    freq1_entry.grid(row=4, column=0, pady=(4,8))
    Tooltip(freq1_entry, "Haz clic para introducir una frecuencia exacta (20-2000 Hz)")

    ttk.Label(osc1_frame, text="Amp").grid(row=0, column=1, padx=(6,0))
    amp1_scale = ttk.Scale(osc1_frame, from_=1.0, to=0.0, orient='vertical',
                           command=lambda v: slider_changed(amp1, amp1_label, "{:.2f}", v))
    amp1_scale.set(amp1.get())
    amp1_scale.grid(row=1, column=1, rowspan=3, padx=(6,0))
    Tooltip(amp1_scale, "Controla el volumen de este oscilador.\nÚsalo para equilibrar ambos osciladores.")
    amp1_entry = crear_entry_amplitud(osc1_frame, amp1, amp1_label, amp1_scale)
    amp1_entry.grid(row=4, column=1, pady=(4,8), padx=(6,0))
    Tooltip(amp1_entry, "Haz clic para introducir una amplitud exacta (0.0-1.0)")

    ttk.Label(osc1_frame, text="Forma:").grid(row=5, column=0, columnspan=2, pady=(6,2))
    combo_forma1 = ttk.Combobox(osc1_frame, textvariable=forma1,
                                values=["sinusoidal", "cuadrada", "triangular", "sierra"], width=12, state="readonly")
    combo_forma1.grid(row=6, column=0, columnspan=2, pady=(0,6))
    combo_forma1.bind("<<ComboboxSelected>>", lambda e: update_callback())
    Tooltip(combo_forma1, "Cambia el la forma de onda del oscilador 1.\nPulsa ? para más información.")

    ttk.Label(osc1_frame, text="Unison (voces):").grid(row=7, column=0, columnspan=2, pady=(6,2))
    unison1_spinbox = ttk.Spinbox(osc1_frame, from_=1, to=8, textvariable=unison1, width=10, command=update_callback)
    unison1_spinbox.grid(row=8, column=0, columnspan=2, pady=(0,6))
    Tooltip(unison1_spinbox, "Cuántas copias del sonido se generan.")

    ttk.Label(osc1_frame, text="Detune (cents):").grid(row=9, column=0, columnspan=2, pady=(6,2))
    def detune1_cb(v):
        detune1.set(float(v))
        tooltip_detune1.update()
        update_callback()
    detune1_knob = Knob(osc1_frame, min_val=0.0, max_val=50.0, initial=detune1.get(), size=44, callback=detune1_cb)
    detune1_knob.grid(row=10, column=0, columnspan=2, pady=(0,6))
    tooltip_detune1 = Tooltip(detune1_knob, lambda: f"Detune: {detune1.get():.1f} cents")

    # Oscilador 2
    ttk.Label(osc2_frame, text="Freq (Hz)").grid(row=0, column=0, pady=(4,0))
    freq2_scale = ttk.Scale(osc2_frame, from_=2000, to=20, orient='vertical',
                            command=lambda v: slider_changed(freq2, freq2_label, "{:.1f} Hz", v))
    freq2_scale.set(freq2.get())
    freq2_scale.grid(row=1, column=0, padx=6, rowspan=3)
    Tooltip(freq2_scale, "Controla qué tan agudo o grave es el sonido del oscilador 2.")
    freq2_entry = crear_entry_frecuencia(osc2_frame, freq2, freq2_label, freq2_scale)
    freq2_entry.grid(row=4, column=0, pady=(4,8))
    Tooltip(freq2_entry, "Haz clic para introducir una frecuencia exacta (20-2000 Hz)")

    ttk.Label(osc2_frame, text="Amp").grid(row=0, column=1, padx=(6,0))
    amp2_scale = ttk.Scale(osc2_frame, from_=1.0, to=0.0, orient='vertical',
                           command=lambda v: slider_changed(amp2, amp2_label, "{:.2f}", v))
    amp2_scale.set(amp2.get())
    amp2_scale.grid(row=1, column=1, rowspan=3, padx=(6,0))
    Tooltip(amp2_scale, "Controla el volumen del oscilador 2.")
    amp2_entry = crear_entry_amplitud(osc2_frame, amp2, amp2_label, amp2_scale)
    amp2_entry.grid(row=4, column=1, pady=(4,8), padx=(6,0))
    Tooltip(amp2_entry, "Haz clic para introducir una amplitud exacta (0.0-1.0)")

    ttk.Label(osc2_frame, text="Forma:").grid(row=5, column=0, columnspan=2, pady=(6,2))
    combo_forma2 = ttk.Combobox(osc2_frame, textvariable=forma2,
                                values=["sinusoidal", "cuadrada", "triangular", "sierra"], width=12, state="readonly")
    combo_forma2.grid(row=6, column=0, columnspan=2, pady=(0,6))
    combo_forma2.bind("<<ComboboxSelected>>", lambda e: update_callback())
    Tooltip(combo_forma2, "Cambia la forma de onda del oscilador 2.")

    ttk.Label(osc2_frame, text="Unison (voces):").grid(row=7, column=0, columnspan=2, pady=(6,2))
    unison2_spinbox = ttk.Spinbox(osc2_frame, from_=1, to=8, textvariable=unison2, width=10, command=update_callback)
    unison2_spinbox.grid(row=8, column=0, columnspan=2, pady=(0,6))
    Tooltip(unison2_spinbox, "Cuántas copias del sonido se generan en el oscilador 2.")

    ttk.Label(osc2_frame, text="Detune (cents):").grid(row=9, column=0, columnspan=2, pady=(6,2))
    def detune2_cb(v):
        detune2.set(float(v))
        tooltip_detune2.update()
        update_callback()
    detune2_knob = Knob(osc2_frame, min_val=0.0, max_val=50.0, initial=detune2.get(), size=44, callback=detune2_cb)
    detune2_knob.grid(row=10, column=0, columnspan=2, pady=(0,6))
    tooltip_detune2 = Tooltip(detune2_knob, lambda: f"Detune: {detune2.get():.1f} cents")


def crear_controles_interaccion(parent, interaccion, fm_index, update_callback):
    """
    Crea los controles de interacción entre osciladores (ninguna, FM, ring_mod, sync).
    """
    texto_ayuda = """Las interacciones combinan los dos osciladores de diferentes formas:

• Ninguna: suma ambos osciladores (suenan juntos sin modificarse).
• FM (modulación en frecuencia): el oscilador 2 modula la frecuencia del 1, creando nuevos armónicos.
  y fm index controla la intesidad de la modulacion.
• Ring Mod: multiplica ambas ondas, genera efectos metálicos o robóticos.
• Sync: el oscilador 2 reinicia la fase del 1, creando un sonido brillante con muchos armónicos.

Consejo: empieza con Ninguna, luego prueba FM con índice bajo y sube poco a poco para oír la diferencia."""
    
    frame, _ = crear_labelframe_con_ayuda(parent, "Interacción entre osciladores", texto_ayuda)
    frame.pack(fill="x", pady=4)

    ttk.Label(frame, text="Tipo:").grid(row=0, column=0, sticky="w", padx=6, pady=6)
    interacciones = ["ninguna", "fm", "ring_mod", "sync"]
    combo_interaccion = ttk.Combobox(frame, textvariable=interaccion, values=interacciones, width=12, state="readonly")
    combo_interaccion.grid(row=0, column=1, padx=6, sticky="w", pady=6)
    combo_interaccion.bind("<<ComboboxSelected>>", lambda e: update_callback())
    Tooltip(combo_interaccion, "Cómo interactúan los osciladores entre sí.\nPulsa ? para más información")

    ttk.Label(frame, text="FM index").grid(row=1, column=0, sticky="w", padx=6, pady=(0,6))
    def fm_cb(v):
        fm_index.set(float(v))
        tooltip_fm.update()
        update_callback()
    fm_knob = Knob(frame, min_val=0.0, max_val=20.0, initial=fm_index.get(), size=44, callback=fm_cb)
    fm_knob.grid(row=1, column=1, padx=6, sticky="w", pady=(0,6))
    tooltip_fm = Tooltip(fm_knob, lambda: f"FM Index: {fm_index.get():.1f}")


def crear_controles_filtrado(parent,filtro_activo,tipo_filtro,cutoff_filtro,bandwidth_filtro,update_callback):
    """
    Crea los controles gráficos del módulo de filtrado.
    """
    texto_ayuda = """El módulo de filtrado modifica el contenido espectral de la señal.

• Activar filtro: aplica o desactiva el filtrado.
• Tipo: selecciona paso bajo, paso alto o paso banda.
• Cutoff: frecuencia de corte del filtro.
• Bandwidth: ancho de banda usado en el filtro paso banda.

El filtro se aplica después de generar o combinar los osciladores."""

    frame, _ = crear_labelframe_con_ayuda(parent, "Filtro", texto_ayuda)
    frame.pack(fill="x", pady=4)

    activar_check = ttk.Checkbutton(frame,text="Activar filtro",variable=filtro_activo,command=update_callback)
    activar_check.grid(row=0, column=0, columnspan=2, sticky="w", padx=6, pady=4)

    ttk.Label(frame, text="Tipo").grid(row=1, column=0, sticky="w", padx=6, pady=4)
    tipo_combo = ttk.Combobox(frame,textvariable=tipo_filtro,values=["lowpass", "highpass", "bandpass"],width=12,state="readonly")
    tipo_combo.grid(row=1, column=1, sticky="ew", padx=6, pady=4)
    tipo_combo.bind("<<ComboboxSelected>>", lambda _e: update_callback())

    ttk.Label(frame, text="Cutoff (Hz)").grid(row=2, column=0, sticky="w", padx=6, pady=4)
    cutoff_scale = ttk.Scale(frame,from_=20.0,to=5000.0,orient="horizontal",variable=cutoff_filtro,command=lambda _v: update_callback())
    cutoff_scale.grid(row=2, column=1, sticky="ew", padx=6, pady=4)

    ttk.Label(frame, text="Bandwidth").grid(row=3, column=0, sticky="w", padx=6, pady=4)
    bandwidth_scale = ttk.Scale(frame,from_=50.0,to=3000.0,orient="horizontal",variable=bandwidth_filtro,command=lambda _v: update_callback())
    bandwidth_scale.grid(row=3, column=1, sticky="ew", padx=6, pady=4)

    frame.grid_columnconfigure(1, weight=1)


def crear_controles_amplificacion(parent,nivel_osc1,nivel_osc2,ganancia,master,normalizar,saturacion,update_callback):
    """
    Crea los controles gráficos del módulo de amplificación y mezcla.
    """
    texto_ayuda = """El módulo de amplificación controla la mezcla y el nivel final de la señal.

• Nivel Osc 1: volumen del oscilador 1 dentro del mezclador.
• Nivel Osc 2: volumen del oscilador 2 dentro del mezclador.
• Ganancia: amplificación antes de la salida final.
• Master: volumen final de salida.
• Normalizar: evita que la señal supere los valores dentro del rango seguro.
• Saturación suave: aplica una distorsión suave usando tanh (tangente hiperbólica).

El mezclador decide cuánto pasa de cada oscilador.
El amplificador decide cómo sale la señal final."""

    frame, _ = crear_labelframe_con_ayuda(parent, "Amplificación y Mezcla", texto_ayuda)
    frame.pack(fill="x", pady=4)

    ttk.Label(frame, text="Nivel Osc 1").grid(row=0, column=0, sticky="w", padx=6, pady=4)
    nivel1_scale = ttk.Scale(frame,from_=0.0,to=1.5,orient="horizontal",variable=nivel_osc1,command=lambda _v: update_callback())
    nivel1_scale.grid(row=0, column=1, padx=6, pady=4, sticky="ew")

    ttk.Label(frame, text="Nivel Osc 2").grid(row=1, column=0, sticky="w", padx=6, pady=4)
    nivel2_scale = ttk.Scale(frame,from_=0.0,to=1.5,orient="horizontal",variable=nivel_osc2,command=lambda _v: update_callback())
    nivel2_scale.grid(row=1, column=1, padx=6, pady=4, sticky="ew")

    ttk.Label(frame, text="Ganancia").grid(row=2, column=0, sticky="w", padx=6, pady=4)
    ganancia_scale = ttk.Scale(frame,from_=0.0,to=3.0,orient="horizontal",variable=ganancia,command=lambda _v: update_callback())
    ganancia_scale.grid(row=2, column=1, padx=6, pady=4, sticky="ew")

    ttk.Label(frame, text="Master").grid(row=3, column=0, sticky="w", padx=6, pady=4)
    master_scale = ttk.Scale(frame,from_=0.0,to=1.0,orient="horizontal",variable=master,command=lambda _v: update_callback())
    master_scale.grid(row=3, column=1, padx=6, pady=4, sticky="ew")

    normalizar_check = ttk.Checkbutton(frame,text="Normalizar",variable=normalizar,command=update_callback)
    normalizar_check.grid(row=4, column=0, padx=6, pady=4, sticky="w")

    saturacion_check = ttk.Checkbutton(frame,text="Saturación suave",variable=saturacion,command=update_callback)
    saturacion_check.grid(row=4, column=1, padx=6, pady=4, sticky="w")

    frame.grid_columnconfigure(1, weight=1)