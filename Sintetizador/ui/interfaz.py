import tkinter as tk
from tkinter import ttk
import numpy as np
import sounddevice as sd

from audio.oscilador import Oscilador
from audio.interacciones import ninguna, fm, ring_mod, sync
from audio.notas import nota_a_frecuencia
from audio.filtros import Filtro
from audio.amplificador import Mezclador, Amplificador
from audio.envolvente import GeneradorEnvolvente

from ui.controles import (crear_controles_osciladores, crear_controles_interaccion,
                          crear_controles_amplificacion, crear_controles_filtrado,
                          crear_controles_envolvente)
from ui.teclado import crear_teclado
from ui.visualizadores import crear_visualizadores
from ui.widgets import Tooltip, crear_labelframe_con_ayuda
from ui.ayuda import mostrar_ayuda, mostrar_guia_inicio
from ui.presets import PRESETS, TEXTO_AYUDA_PRESETS

class SintetizadorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sintetizador Didáctico")
        self.geometry("1700x950")
        self.resizable(False, False)

        self.duracion_visual = 0.01
        self.duracion_audio = 0.5
        self.sample_rate = 44100

        self.osc1 = Oscilador(sample_rate=self.sample_rate)
        self.osc2 = Oscilador(frecuencia=440, forma='cuadrada', amplitud=0.5, sample_rate=self.sample_rate)

        self.interaccion = tk.StringVar(value="ninguna")
        self.onda_comb = None

        self.freq1 = tk.DoubleVar(value=440.0)
        self.amp1 = tk.DoubleVar(value=0.5)
        self.forma1 = tk.StringVar(value="sinusoidal")
        self.unison1 = tk.IntVar(value=1)
        self.detune1 = tk.DoubleVar(value=10.0)

        self.freq2 = tk.DoubleVar(value=440.0)
        self.amp2 = tk.DoubleVar(value=0.5)
        self.forma2 = tk.StringVar(value="cuadrada")
        self.unison2 = tk.IntVar(value=1)
        self.detune2 = tk.DoubleVar(value=10.0)

        self.fm_index = tk.DoubleVar(value=5.0)
        self.preset = tk.StringVar(value="Init")

        self.filtro_activo = tk.BooleanVar(value=False)
        self.tipo_filtro = tk.StringVar(value="lowpass")
        self.cutoff_filtro = tk.DoubleVar(value=1000.0)
        self.bandwidth_filtro = tk.DoubleVar(value=500.0)

        self.filtro = Filtro(
            tipo=self.tipo_filtro.get(),
            cutoff=self.cutoff_filtro.get(),
            sample_rate=self.sample_rate,
            bandwidth=self.bandwidth_filtro.get()
        )

        self.nivel_osc1 = tk.DoubleVar(value=1.0)
        self.nivel_osc2 = tk.DoubleVar(value=1.0)
        self.ganancia = tk.DoubleVar(value=1.0)
        self.volumen_master = tk.DoubleVar(value=0.8)
        self.normalizar = tk.BooleanVar(value=True)
        self.saturacion = tk.BooleanVar(value=False)

        self.mezclador = Mezclador(nivel_osc1=self.nivel_osc1.get(), nivel_osc2=self.nivel_osc2.get())

        self.amplificador = Amplificador(
            ganancia= self.ganancia.get(),
            master=self.volumen_master.get(),
            normalizar=self.normalizar.get(),
            saturacion=self.saturacion.get())
        
        self.tipo_envolvente = tk.StringVar(value="gate")
        self.attack = tk.DoubleVar(value=0.05)
        self.decay = tk.DoubleVar(value=0.15)
        self.sustain = tk.DoubleVar(value=0.7)
        self.release = tk.DoubleVar(value=0.2)

        self.envolvente = GeneradorEnvolvente(
            tipo=self.tipo_envolvente.get(),
            attack=self.attack.get(),
            decay=self.decay.get(),
            sustain=self.sustain.get(),
            release=self.release.get(),
            sample_rate=self.sample_rate
        )

        self.left_frame = ttk.Frame(self)
        self.left_frame.place(x=10, y=10, width=420, height=790)

        self.middle_frame = ttk.Frame(self)
        self.middle_frame.place(x=445, y=10, width=300, height=920)

        self.visual_frame = ttk.Frame(self)
        self.visual_frame.place(x=760, y=10, width=730, height=790)

        # columna izquierda con generación de ondas
        crear_controles_osciladores(self.left_frame,self.freq1,self.amp1,self.forma1,self.unison1,self.detune1,
                                    self.freq2,self.amp2,self.forma2,self.unison2,self.detune2,
                                    lambda: self.after_idle(self.actualizar_onda))

        #columna central con interacciones, amplificación y filtrado
        crear_controles_interaccion(self.middle_frame,self.interaccion,self.fm_index,
                                    lambda: self.after_idle(self.actualizar_onda))

        crear_controles_filtrado(self.middle_frame,self.filtro_activo,self.tipo_filtro,self.cutoff_filtro,self.bandwidth_filtro,
                                lambda: self.after_idle(self.actualizar_onda))

        crear_controles_amplificacion(self.middle_frame,self.nivel_osc1,self.nivel_osc2,self.ganancia,self.volumen_master,
                                      self.normalizar,self.saturacion,
                                      lambda: self.after_idle(self.actualizar_onda))
        crear_controles_envolvente(self.middle_frame,self.tipo_envolvente,self.attack,self.decay,self.sustain,self.release,
                                   lambda: self.after_idle(self.actualizar_onda))

        self.crear_botones(self.middle_frame)

        self.key_map = {}
        self.note_to_rect = {}
        self.keyboard_canvas, self.keyboard_hbar = crear_teclado(self.middle_frame,self.key_map,self.note_to_rect,self.tocar_nota)

        # columna derecha con graficos
        self.fig1, self.ax1, self.canvas1, self.fig2, self.ax2, self.canvas2, self.fig3, self.ax3, self.canvas3 = crear_visualizadores(self)

        # Logo del aplicativo
        self.logo_canvas = tk.Canvas(self, width=350, height=80, bg='#2c3e50', highlightthickness=0)
        self.logo_canvas.place(x=950, y=570)
        self.logo_canvas.create_line(15, 40, 25, 30, 35, 50, 45, 30, 55, 40, 65, 30, 75, 50, 85, 30, 95, 40, 
                                      fill="white", width=2, smooth=True)
        self.logo_canvas.create_text(175, 40, text="Sintetizador\nDidáctico", 
                                      font=("Helvetica", 18, "bold italic"), fill="white", anchor="center")
        self.logo_canvas.create_line(270, 40, 280, 25, 290, 55, 300, 25, 310, 55, 320, 25, 330, 40, 
                                      fill="white", width=2)
        self.logo_canvas.create_rectangle(5, 5, 345, 75, outline="#34495e", width=2, fill="")

        self.update_idletasks()
        self.after(60, self.actualizar_onda)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def crear_botones(self, parent):
        """Crea panel de controles generales: presets, reproducción y guía."""
        frame, _ = crear_labelframe_con_ayuda(parent, "Controles Generales", TEXTO_AYUDA_PRESETS)
        frame.pack(side="top", fill="x", padx=5, pady=5)
        
        controles_frame = ttk.Frame(frame)
        controles_frame.pack(fill="x", padx=6, pady=6)

        # Presets
        ttk.Label(controles_frame, text="Preset:").pack(side="left", padx=(0,4))
        self.preset_combo = ttk.Combobox(controles_frame, textvariable=self.preset,
                                         values=list(PRESETS.keys()), width=16, state="readonly")
        self.preset_combo.pack(side="left")
        self.preset_combo.bind("<<ComboboxSelected>>", self._on_preset_change)
        Tooltip(self.preset_combo, "Selecciona un preset didáctico.\nSe cargarán parámetros y verás el efecto en las gráficas.")

        # Reproducir
        btn_play = ttk.Button(controles_frame, text="Reproducir sonido", command=self.reproducir_onda)
        btn_play.pack(side="left", padx=8)
        Tooltip(btn_play, "Reproduce la onda combinada actual con los parámetros seleccionados.")

        # Botón "Cómo empezar"
        btn_inicio = ttk.Button(controles_frame, text="Cómo empezar", command=lambda: mostrar_guia_inicio(self))
        btn_inicio.pack(side="right", padx=4)
        Tooltip(btn_inicio, "Guía paso a paso para crear tu primer sonido desde cero.")

    def _on_preset_change(self, _evt=None):
        """Aplica el preset seleccionado al cambiar en el combobox."""
        self.aplicar_preset(self.preset.get())

    def aplicar_preset(self, nombre):
        """Carga parámetros del preset especificado."""
        p = PRESETS.get(nombre)
        if not p:
            return
        self.freq1.set(p["f1"]); self.amp1.set(p["a1"]); self.forma1.set(p["w1"]); self.unison1.set(p["u1"]); self.detune1.set(p["d1"])
        self.freq2.set(p["f2"]); self.amp2.set(p["a2"]); self.forma2.set(p["w2"]); self.unison2.set(p["u2"]); self.detune2.set(p["d2"])
        self.interaccion.set(p["ix"]); self.fm_index.set(p["fm"])
        self.after_idle(self.actualizar_onda)

    def tocar_nota(self, note_name):
        """Reproduce sonido con la frecuencia correspondiente a una nota musical."""
        f1_prev = self.osc1.frecuencia
        f2_prev = self.osc2.frecuencia
        f_note = nota_a_frecuencia(note_name)

        osc1_loc = Oscilador(frecuencia=f_note, amplitud=self.amp1.get(), forma=self.forma1.get(),
                             fase=getattr(self.osc1, 'fase', 0.0), sample_rate=self.sample_rate,
                             unison=self.unison1.get(), detune_cents=self.detune1.get())
        osc2_loc = Oscilador(frecuencia=self.freq2.get(), amplitud=self.amp2.get(), forma=self.forma2.get(),
                             fase=getattr(self.osc2, 'fase', 0.0), sample_rate=self.sample_rate,
                             unison=self.unison2.get(), detune_cents=self.detune2.get())
        
        self.mezclador.set_nivel_osc1(self.nivel_osc1.get())
        self.mezclador.set_nivel_osc2(self.nivel_osc2.get())

        self.amplificador.set_ganancia(self.ganancia.get())
        self.amplificador.set_master(self.volumen_master.get())
        self.amplificador.set_normalizar(self.normalizar.get())
        self.amplificador.set_saturacion(self.saturacion.get())

        self.envolvente.set_tipo(self.tipo_envolvente.get())
        self.envolvente.set_attack(self.attack.get())
        self.envolvente.set_decay(self.decay.get())
        self.envolvente.set_sustain(self.sustain.get())
        self.envolvente.set_release(self.release.get())

        if self.interaccion.get() == "ninguna":
            onda1_vis = osc1_loc.generar(self.duracion_visual)
            onda2_vis = osc2_loc.generar(self.duracion_visual)
            onda_comb_vis = self.mezclador.mezclar(onda1_vis, onda2_vis)
        elif self.interaccion.get() == "fm":
            onda_comb_vis = fm(osc1_loc, osc2_loc, self.duracion_visual, indice=self.fm_index.get())
        elif self.interaccion.get() == "ring_mod":
            onda_comb_vis = ring_mod(osc1_loc, osc2_loc, self.duracion_visual)
        elif self.interaccion.get() == "sync":
            onda_comb_vis = sync(osc1_loc, osc2_loc, self.duracion_visual)
        else:
            onda_comb_vis = osc1_loc.generar(self.duracion_visual)

        self.filtro.set_tipo(self.tipo_filtro.get())
        self.filtro.set_cutoff(self.cutoff_filtro.get())
        self.filtro.set_bandwidth(self.bandwidth_filtro.get())

        if self.filtro_activo.get():
            onda_comb_vis = self.filtro.aplicar(onda_comb_vis)

        onda_comb_vis = self.envolvente.aplicar(onda_comb_vis)
        onda_comb_vis = self.amplificador.amplificar(onda_comb_vis)

        onda1_vis = osc1_loc.generar(self.duracion_visual)
        onda2_vis = osc2_loc.generar(self.duracion_visual)
        tiempo = np.arange(len(onda1_vis)) / self.sample_rate

        self.ax1.clear()
        self.ax1.set_title("Oscilador 1", fontsize=14, fontweight='bold', pad=10)
        self.ax1.set_xlabel("Tiempo (s)", fontsize=9)
        self.ax1.set_ylabel("Amplitud", fontsize=9)
        self.ax1.plot(tiempo, onda1_vis, color='blue')
        self.ax1.set_xlim(0, self.duracion_visual)
        self.ax1.grid(True)
        self.fig1.subplots_adjust(bottom=0.18, top=0.85)
        self.fig1.tight_layout()
        self.canvas1.draw()

        self.ax2.clear()
        self.ax2.set_title("Oscilador 2", fontsize=14, fontweight='bold', pad=10)
        self.ax2.set_xlabel("Tiempo (s)", fontsize=9)
        self.ax2.set_ylabel("Amplitud", fontsize=9)
        self.ax2.plot(tiempo, onda2_vis, color='green')
        self.ax2.set_xlim(0, self.duracion_visual)
        self.ax2.grid(True)
        self.fig2.subplots_adjust(bottom=0.18, top=0.85)
        self.fig2.tight_layout()
        self.canvas2.draw()

        self.ax3.clear()
        self.ax3.set_title("Onda Combinada", fontsize=14, fontweight='bold', pad=10)
        self.ax3.set_xlabel("Tiempo (s)", fontsize=9)
        self.ax3.set_ylabel("Amplitud", fontsize=9)
        self.ax3.plot(tiempo, onda_comb_vis, color='red')
        self.ax3.set_xlim(0, self.duracion_visual)
        self.ax3.grid(True)
        self.fig3.subplots_adjust(bottom=0.18, top=0.85)
        self.fig3.tight_layout()
        self.canvas3.draw()

        if self.interaccion.get() == "ninguna":
            onda1_play = osc1_loc.generar(self.duracion_audio)
            onda2_play = osc2_loc.generar(self.duracion_audio)
            onda_play = self.mezclador.mezclar(onda1_play, onda2_play)
        elif self.interaccion.get() == "fm":
            onda_play = fm(osc1_loc, osc2_loc, self.duracion_audio, indice=self.fm_index.get())
        elif self.interaccion.get() == "ring_mod":
            onda_play = ring_mod(osc1_loc, osc2_loc, self.duracion_audio)
        elif self.interaccion.get() == "sync":
            onda_play = sync(osc1_loc, osc2_loc, self.duracion_audio)
        else:
            onda_play = osc1_loc.generar(self.duracion_audio)

        self.filtro.set_tipo(self.tipo_filtro.get())
        self.filtro.set_cutoff(self.cutoff_filtro.get())
        self.filtro.set_bandwidth(self.bandwidth_filtro.get())

        if self.filtro_activo.get():
            onda_play = self.filtro.aplicar(onda_play)

        onda_play = self.envolvente.aplicar(onda_play)
        onda_play = self.amplificador.amplificar(onda_play)

        sd.play(onda_play, self.sample_rate)
        sd.wait()

        self.osc1.set_frecuencia(f1_prev)
        self.osc2.set_frecuencia(f2_prev)
        self.actualizar_onda()

    def actualizar_onda(self):
        self.osc1.set_frecuencia(self.freq1.get())
        self.osc1.set_amplitud(self.amp1.get())
        self.osc1.set_forma(self.forma1.get())
        self.osc1.set_unison(self.unison1.get())
        self.osc1.set_detune(self.detune1.get())

        self.osc2.set_frecuencia(self.freq2.get())
        self.osc2.set_amplitud(self.amp2.get())
        self.osc2.set_forma(self.forma2.get())
        self.osc2.set_unison(self.unison2.get())
        self.osc2.set_detune(self.detune2.get())

        self.filtro.set_tipo(self.tipo_filtro.get())
        self.filtro.set_cutoff(self.cutoff_filtro.get())
        self.filtro.set_bandwidth(self.bandwidth_filtro.get())

        self.mezclador.set_nivel_osc1(self.nivel_osc1.get())
        self.mezclador.set_nivel_osc2(self.nivel_osc2.get())

        self.amplificador.set_ganancia(self.ganancia.get())
        self.amplificador.set_master(self.volumen_master.get())
        self.amplificador.set_normalizar(self.normalizar.get())
        self.amplificador.set_saturacion(self.saturacion.get())

        self.envolvente.set_tipo(self.tipo_envolvente.get())
        self.envolvente.set_attack(self.attack.get())
        self.envolvente.set_decay(self.decay.get())
        self.envolvente.set_sustain(self.sustain.get())
        self.envolvente.set_release(self.release.get())

        onda1 = self.osc1.generar(self.duracion_visual)
        onda2 = self.osc2.generar(self.duracion_visual)

        if self.interaccion.get() == "ninguna":
            onda_comb = self.mezclador.mezclar(onda1, onda2)
        elif self.interaccion.get() == "fm":
            onda_comb = fm(self.osc1, self.osc2, self.duracion_visual, indice=self.fm_index.get())
        elif self.interaccion.get() == "ring_mod":
            onda_comb = ring_mod(self.osc1, self.osc2, self.duracion_visual)
        elif self.interaccion.get() == "sync":
            onda_comb = sync(self.osc1, self.osc2, self.duracion_visual)
        else:
            onda_comb = onda1

        if self.filtro_activo.get():
            onda_comb = self.filtro.aplicar(onda_comb)
        
        onda_comb = self.envolvente.aplicar(onda_comb)
        onda_comb = self.amplificador.amplificar(onda_comb)

        onda1_audio = self.osc1.generar(self.duracion_audio)
        onda2_audio = self.osc2.generar(self.duracion_audio)

        if self.interaccion.get() == "ninguna":
            self.onda_comb = self.mezclador.mezclar(onda1_audio, onda2_audio)
        elif self.interaccion.get() == "fm":
            self.onda_comb = fm(self.osc1, self.osc2, self.duracion_audio, indice=self.fm_index.get())
        elif self.interaccion.get() == "ring_mod":
            self.onda_comb = ring_mod(self.osc1, self.osc2, self.duracion_audio)
        elif self.interaccion.get() == "sync":
            self.onda_comb = sync(self.osc1, self.osc2, self.duracion_audio)
        else:
            self.onda_comb = self.osc1.generar(self.duracion_audio)

        if self.filtro_activo.get():
            self.onda_comb = self.filtro.aplicar(self.onda_comb)

        self.onda_comb = self.envolvente.aplicar(self.onda_comb)
        self.onda_comb = self.amplificador.amplificar(self.onda_comb)
        
        tiempo = np.arange(len(onda1)) / self.sample_rate

        self.ax1.clear()
        self.ax1.set_title("Oscilador 1", fontsize=14, fontweight='bold', pad=10)
        self.ax1.set_xlabel("Tiempo (s)", fontsize=9)
        self.ax1.set_ylabel("Amplitud", fontsize=9)
        self.ax1.plot(tiempo, onda1, color='blue')
        self.ax1.set_xlim(0, self.duracion_visual)
        self.ax1.grid(True)
        self.fig1.subplots_adjust(bottom=0.18, top=0.85)
        self.fig1.tight_layout()
        self.canvas1.draw()

        self.ax2.clear()
        self.ax2.set_title("Oscilador 2", fontsize=14, fontweight='bold', pad=10)
        self.ax2.set_xlabel("Tiempo (s)", fontsize=9)
        self.ax2.set_ylabel("Amplitud", fontsize=9)
        self.ax2.plot(tiempo, onda2, color='green')
        self.ax2.set_xlim(0, self.duracion_visual)
        self.ax2.grid(True)
        self.fig2.subplots_adjust(bottom=0.18, top=0.85)
        self.fig2.tight_layout()
        self.canvas2.draw()

        self.ax3.clear()
        self.ax3.set_title("Onda Combinada", fontsize=14, fontweight='bold', pad=10)
        self.ax3.set_xlabel("Tiempo (s)", fontsize=9)
        self.ax3.set_ylabel("Amplitud", fontsize=9)
        self.ax3.plot(tiempo, onda_comb, color='red')
        self.ax3.set_xlim(0, self.duracion_visual)
        self.ax3.grid(True)
        self.fig3.subplots_adjust(bottom=0.18, top=0.85)
        self.fig3.tight_layout()
        self.canvas3.draw()

    def reproducir_onda(self):
        if self.onda_comb is not None:
            print(f"Reproduciendo audio en dispositivo: {sd.default.device}")
            sd.play(self.onda_comb, self.sample_rate)
            sd.wait()

    def on_closing(self):
        """Limpia recursos y cierra la aplicación correctamente."""
        try:
            sd.stop()
        except Exception:
            pass
        self.quit()

