import numpy as np
from audio.oscilador import Oscilador


def ninguna(osc1, osc2, duracion):
    """Sin interacción: solo suma las ondas."""
    return osc1.generar(duracion) + osc2.generar(duracion)

def fm(osc1, osc2, duracion, indice=5.0):
    """Modulación en frecuencia: osc2 modula la frecuencia de osc1."""
    n_muestras = int(osc1.sample_rate * duracion)
    t = np.linspace(0, duracion, n_muestras, endpoint=False)
    moduladora = osc2.generar(duracion)
    fase_instantanea = 2 * np.pi * osc1.frecuencia * t + indice * moduladora
    
    if osc1.forma == 'sinusoidal':
        onda_fm = osc1.amplitud * np.sin(fase_instantanea + osc1.fase)
    elif osc1.forma == 'cuadrada':
        onda_fm = osc1.amplitud * np.sign(np.sin(fase_instantanea + osc1.fase))
    elif osc1.forma == 'triangular':
        onda_fm = osc1.amplitud * (2 / np.pi) * np.arcsin(np.sin(fase_instantanea + osc1.fase))
    elif osc1.forma == 'sierra':
        onda_fm = osc1.amplitud * 2 * ((fase_instantanea + osc1.fase) / (2 * np.pi) - np.floor((fase_instantanea + osc1.fase) / (2 * np.pi) + 0.5))
    else:
        onda_fm = osc1.amplitud * np.sin(fase_instantanea + osc1.fase)
    return onda_fm

def ring_mod(osc1, osc2, duracion):
    """Modulación en anillo: multiplica las dos ondas."""
    return osc1.generar(duracion) * osc2.generar(duracion)

def sync(osc1, osc2, duracion):
    """Sincronización: osc2 reinicia la fase de osc1."""
    n_muestras = int(osc1.sample_rate * duracion)
    t = np.linspace(0, duracion, n_muestras, endpoint=False)
    onda2 = osc2.generar(duracion)
    fase_acumulada = np.zeros(n_muestras)
    fase_actual = osc1.fase
    for i in range(1, n_muestras):
        if onda2[i-1] < 0 and onda2[i] >= 0:
            fase_actual = 0
        fase_actual += 2 * np.pi * osc1.frecuencia / osc1.sample_rate
        fase_acumulada[i] = fase_actual
    if osc1.forma == 'sinusoidal':
        return osc1.amplitud * np.sin(fase_acumulada)
    elif osc1.forma == 'cuadrada':
        return osc1.amplitud * np.sign(np.sin(fase_acumulada))
    elif osc1.forma == 'triangular':
        return osc1.amplitud * (2 / np.pi) * np.arcsin(np.sin(fase_acumulada))
    elif osc1.forma == 'sierra':
        return osc1.amplitud * 2 * (fase_acumulada / (2 * np.pi) - np.floor(fase_acumulada / (2 * np.pi) + 0.5))
    else:
        return osc1.amplitud * np.sin(fase_acumulada)

# Ejemplo de uso (para pruebas):
if __name__ == "__main__":
    osc1 = Oscilador(frecuencia=440, forma='sinusoidal')
    osc2 = Oscilador(frecuencia=442, forma='cuadrada', amplitud=0.5)
    duracion = 1.0
    onda_fm = fm(osc1, osc2, duracion, indice=5.0)
    onda_ring = ring_mod(osc1, osc2, duracion)
    onda_sync = sync(osc1, osc2, duracion)
    print("Interacciones generadas correctamente.")