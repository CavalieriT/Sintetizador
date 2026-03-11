import tkinter as tk
import math
from tkinter import ttk

class Knob(tk.Canvas):
    """
    Knob simple: arrastra verticalmente para cambiar valor.
    Rango: min_val .. max_val. Llama callback(value) con valor actual.
    Apariencia: fondo negro, indicador blanco.
    """
    def __init__(self, master, min_val=0.0, max_val=1.0, initial=0.0, size=48, callback=None, **kwargs):
        try:
            bg = master.cget('background')
        except Exception:
            try:
                bg = master['bg']
            except Exception:
                bg = 'SystemButtonFace'
        super().__init__(master, width=size, height=size, bg=bg, highlightthickness=0, **kwargs)
        self.size = size
        self.center = size // 2
        self.radius = int(size * 0.38)
        self.min_val = min_val
        self.max_val = max_val
        self.callback = callback
        self.value = initial
        self.min_angle = -135
        self.max_angle = 135
        self.angle = self._val_to_angle(initial)
        self._draw_knob()
        self.bind("<Button-1>", self._start)
        self.bind("<B1-Motion>", self._drag)
        self.bind("<ButtonRelease-1>", self._release)

    def _draw_knob(self):
        self.delete("all")
        self.create_oval(self.center - self.radius, self.center - self.radius,
                         self.center + self.radius, self.center + self.radius,
                         fill='black', outline='dim gray', width=1)
        ang_rad = math.radians(self.angle)
        x = self.center + int(self.radius * 0.7 * math.cos(ang_rad))
        y = self.center + int(self.radius * 0.7 * math.sin(ang_rad))
        self.create_line(self.center, self.center, x, y, fill='white', width=3, capstyle='round')
        self.create_oval(self.center - 3, self.center - 3, self.center + 3, self.center + 3, fill='white', outline='')

    def _val_to_angle(self, val):
        t = (val - self.min_val) / (self.max_val - self.min_val) if self.max_val != self.min_val else 0.0
        return self.min_angle + t * (self.max_angle - self.min_angle)

    def _angle_to_val(self, angle):
        t = (angle - self.min_angle) / (self.max_angle - self.min_angle)
        return self.min_val + t * (self.max_val - self.min_val)

    def _start(self, event):
        self._last_y = event.y

    def _drag(self, event):
        dy = self._last_y - event.y
        delta_angle = dy * 0.8
        self.angle = max(self.min_angle, min(self.max_angle, self.angle + delta_angle))
        self._last_y = event.y
        self.value = self._angle_to_val(self.angle)
        if self.callback:
            try:
                self.callback(self.value)
            except Exception:
                pass
        self._draw_knob()

    def _release(self, event):
        return

class Tooltip:
    def __init__(self, widget, text, delay=500, wraplength=300):
        self.widget = widget
        self.text_func = text if callable(text) else lambda: text
        self.delay = delay
        self.wraplength = wraplength
        self._id = None
        self._tip = None
        self.widget.bind("<Enter>", self._on_enter, add="+")
        self.widget.bind("<Leave>", self._on_leave, add="+")
        self.widget.bind("<Motion>", self._on_motion, add="+")

    def _on_enter(self, _event):
        self._schedule()

    def _on_leave(self, _event):
        self._unschedule()
        self._hide()

    def _on_motion(self, _event):
        self._unschedule()
        self._schedule()

    def _schedule(self):
        self._id = self.widget.after(self.delay, self._show)

    def _unschedule(self):
        if self._id:
            try:
                self.widget.after_cancel(self._id)
            except Exception:
                pass
            self._id = None

    def _show(self):
        if self._tip:
            return
        x = self.widget.winfo_rootx() + 12
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 8
        self._tip = tk.Toplevel(self.widget)
        self._tip.wm_overrideredirect(True)
        self._tip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self._tip, text=self.text_func(), justify="left",
                         background="#ffffe0", relief="solid", borderwidth=1,
                         wraplength=self.wraplength)
        label.pack(ipadx=6, ipady=4)

    def _hide(self):
        if self._tip:
            try:
                self._tip.destroy()
            except Exception:
                pass
            self._tip = None

    def update(self):
        """Actualiza el texto del tooltip si está visible."""
        if self._tip:
            try:
                label = self._tip.winfo_children()[0]
                label.config(text=self.text_func())
            except Exception:
                pass

class HelpPopup:
    """
    Popup de ayuda ampliado que aparece al hacer clic en un botón '?'
    """
    def __init__(self, parent, title, text):
        self.parent = parent
        self.title = title
        self.text = text
    
    def show(self):
        win = tk.Toplevel(self.parent)
        win.title(self.title)
        win.geometry("500x350")
        win.resizable(False, False)
        
        frm = ttk.Frame(win, padding=10)
        frm.pack(fill="both", expand=True)
        
        txt = tk.Text(frm, wrap="word", font=("Arial", 10), bg="#f9f9f9", relief="flat")
        scr = ttk.Scrollbar(frm, orient="vertical", command=txt.yview)
        txt.configure(yscrollcommand=scr.set)
        txt.insert("1.0", self.text)
        txt.configure(state="disabled")
        
        txt.pack(side="left", fill="both", expand=True)
        scr.pack(side="right", fill="y")
        
        btn = ttk.Button(win, text="Cerrar", command=win.destroy)
        btn.pack(pady=8)

def crear_labelframe_con_ayuda(parent, texto_titulo, texto_ayuda, **kwargs):
    """
    Crea un LabelFrame con un botón de ayuda '?' integrado en el título.
    Retorna (frame, boton_ayuda)
    """
    # Frame contenedor para el título personalizado
    frame = ttk.LabelFrame(parent, **kwargs)
    
    # Frame interno para el título con botón
    title_frame = tk.Frame(frame)
    frame.configure(labelwidget=title_frame)
    
    # Etiqueta del título
    ttk.Label(title_frame, text=texto_titulo, font=("TkDefaultFont", 9)).pack(side="left", padx=(0, 4))
    
    # Botón de ayuda pequeño
    btn = tk.Label(title_frame, text="?", font=("Arial", 8, "bold"),
                   fg="white", bg="#5a9bd4", width=1, relief="raised",
                   cursor="hand2", padx=2, pady=0, borderwidth=1)
    btn.pack(side="left")
    
    popup = HelpPopup(parent, f"Ayuda: {texto_titulo}", texto_ayuda)
    btn.bind("<Button-1>", lambda e: popup.show())
    
    # Efecto hover
    btn.bind("<Enter>", lambda e: btn.config(bg="#4080c0"))
    btn.bind("<Leave>", lambda e: btn.config(bg="#5a9bd4"))
    
    return frame, btn