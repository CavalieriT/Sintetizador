import tkinter as tk
from tkinter import ttk
from audio.notas import NOTAS_FRECUENCIAS  # <<< LÍNEA AÑADIDA
from ui.widgets import crear_labelframe_con_ayuda

def crear_teclado(parent, key_map, note_to_rect, tocar_callback):
    texto_ayuda_teclado = """El teclado virtual te permite tocar notas con el ratón.

• Haz clic en una tecla para escuchar la nota correspondiente.
• Las teclas blancas son notas naturales (C, D, E, F, G, A, B).
• Las teclas negras son sostenidos (#).
• El teclado cubre varias octavas (grupos de 12 semitonos).

Consejo: antes de tocar, ajusta los osciladores y la interacción para crear diferentes sonidos. Luego toca notas para oírlos en diferentes tonos."""
    
    frame, _ = crear_labelframe_con_ayuda(parent, "Teclado Virtual", texto_ayuda_teclado)
    frame.pack(side="top", fill="x", pady=6)

    # Contenedor con altura fija
    container = tk.Frame(frame, height=110)
    container.pack(side="top", fill="x", padx=4, pady=4)
    container.pack_propagate(False)

    canvas = tk.Canvas(container, bg='white', highlightthickness=0)
    hbar = ttk.Scrollbar(container, orient='horizontal', command=canvas.xview)
    canvas.config(xscrollcommand=hbar.set)
    
    hbar.pack(side='bottom', fill='x')
    canvas.pack(side='top', fill='both', expand=True)

    octaves = 4
    start_octave = 2
    white_width = 22
    white_height = 80
    black_width = 14
    black_height = 50
    x_offset = 10
    y_top = 8

    notes_per_octave = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    white_notes = ['C','D','E','F','G','A','B']

    # Dibujar teclas blancas
    for octave in range(start_octave, start_octave + octaves):
        for i, note_name in enumerate(white_notes):
            full_note = f"{note_name}{octave}"
            x1 = x_offset
            y1 = y_top
            x2 = x1 + white_width
            y2 = y1 + white_height
            
            # Rectángulo visible (blanco)
            rect_id = canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='black', width=2)
            note_to_rect[full_note] = rect_id
            key_map[rect_id] = full_note
            
            # Rectángulo invisible expandido (mejor área de click)
            invisible_id = canvas.create_rectangle(x1-2, y1-5, x2+2, y2+5, 
                                                    fill='', outline='', activefill='')
            key_map[invisible_id] = full_note
            
            # Etiqueta de texto (IMPORTANTE: registrarlo también en key_map)
            text_x = x1 + white_width // 2
            text_y = y2 - 10
            text_id = canvas.create_text(text_x, text_y, text=full_note, font=("Arial", 7), fill="black")
            key_map[text_id] = full_note  # <<< LÍNEA AÑADIDA
            
            x_offset += white_width

    # Dibujar teclas negras
    x_offset = 10
    black_positions = [0.7, 1.7, 3.7, 4.7, 5.7]
    for octave in range(start_octave, start_octave + octaves):
        for bp in black_positions:
            idx = int(bp)
            if idx < len(white_notes):
                base_note = white_notes[idx]
                full_note = f"{base_note}#{octave}"
                x1 = x_offset + int(bp * white_width) - black_width // 2
                y1 = y_top
                x2 = x1 + black_width
                y2 = y1 + black_height
                
                # Rectángulo visible (negro)
                rect_id = canvas.create_rectangle(x1, y1, x2, y2, fill='black', outline='black')
                note_to_rect[full_note] = rect_id
                key_map[rect_id] = full_note
                
                # Rectángulo invisible expandido
                invisible_id = canvas.create_rectangle(x1-2, y1-3, x2+2, y2+3,
                                                        fill='', outline='', activefill='')
                key_map[invisible_id] = full_note
                
        x_offset += 7 * white_width

    canvas.config(scrollregion=canvas.bbox("all"))

    def on_click(event):
        x_canvas = canvas.canvasx(event.x)
        y_canvas = canvas.canvasy(event.y)
        item = canvas.find_overlapping(x_canvas, y_canvas, x_canvas, y_canvas)
        if item:
            rect_id = item[-1]
            if rect_id in key_map:
                note = key_map[rect_id]
                tocar_callback(note)

    canvas.bind("<Button-1>", on_click)
    return canvas, hbar