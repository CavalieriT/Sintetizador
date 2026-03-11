"""
Módulo de gestión de presets del sintetizador.
Contiene configuraciones predefinidas para diferentes tipos de sonidos.
"""

# Diccionario de presets
PRESETS = {
    "Init": {
        "f1": 440.0, "a1": 0.5, "w1": "sinusoidal", "u1": 1, "d1": 0.0,  # Cambiado a1 de 1.0 a 0.5
        "f2": 440.0, "a2": 0.5, "w2": "cuadrada",   "u2": 1, "d2": 0.0,
        "ix": "ninguna", "fm": 3.0
    },
    "Unison Lead": {
        "f1": 440.0, "a1": 0.9, "w1": "sierra",     "u1": 5, "d1": 12.0,
        "f2": 440.0, "a2": 0.4, "w2": "cuadrada",   "u2": 3, "d2": 8.0,
        "ix": "ninguna", "fm": 0.0
    },
    "FM Bell": {
        "f1": 440.0, "a1": 0.8, "w1": "sinusoidal", "u1": 1, "d1": 0.0,
        "f2": 440.0, "a2": 0.7, "w2": "sinusoidal", "u2": 1, "d2": 0.0,
        "ix": "fm",   "fm": 9.0
    },
    "Ring Metal": {
        "f1": 440.0, "a1": 0.9, "w1": "cuadrada",   "u1": 1, "d1": 0.0,
        "f2": 660.0, "a2": 0.7, "w2": "sierra",     "u2": 1, "d2": 0.0,
        "ix": "ring_mod", "fm": 0.0
    },
    "Sync Bright": {
        "f1": 440.0, "a1": 0.9, "w1": "sierra",     "u1": 1, "d1": 0.0,
        "f2": 880.0, "a2": 0.6, "w2": "cuadrada",   "u2": 1, "d2": 0.0,
        "ix": "sync", "fm": 0.0
    },
}

# Texto de ayuda para presets
TEXTO_AYUDA_PRESETS = """Los presets son configuraciones predefinidas que cargan parámetros específicos:

• Init: punto de partida limpio, sonidos básicos.
• Unison Lead: sonido ancho ideal para melodías principales (varias voces con detune).
• FM Bell: sonido de campana usando modulación FM.
• Ring Metal: efecto metálico con modulación en anillo.
• Sync Bright: sonido brillante con sincronización.

Consejo: carga un preset, observa las gráficas y luego modifica los parámetros para entender qué hace cada uno."""