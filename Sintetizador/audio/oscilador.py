import numpy as np

class Oscilador:
    """
    Generador de formas de onda para síntesis de audio.
    
    Soporta: sinusoidal, triangular, sierra y cuadrada.
    Incluye características de unison (múltiples voces) y detune (desafinación).
    
    Atributos:
        frecuencia: Frecuencia base en Hz
        amplitud: Volumen (0.0 a 1.0)
        forma: Tipo de onda ('sinusoidal', 'cuadrada', 'triangular', 'sierra')
        fase: Fase inicial en radianes
        sample_rate: Frecuencia de muestreo en Hz
        unison: Número de voces desafinadas
        detune_cents: Desafinación en cents (centésimas de semitono)
    """

    def __init__(self, frecuencia=440, amplitud=0.5, forma='sinusoidal', fase=0.0, sample_rate=44100, unison=1, detune_cents=0.0):
        self.frecuencia = frecuencia
        self.amplitud = amplitud
        self.forma = forma
        self.fase = fase
        self.sample_rate = sample_rate
        self.unison = unison  # número de voces
        self.detune_cents = detune_cents  # desafinación en cents

    def set_frecuencia(self, nueva_frecuencia):
        self.frecuencia = nueva_frecuencia

    def set_amplitud(self, nueva_amplitud):
        self.amplitud = nueva_amplitud

    def set_forma(self, nueva_forma):
        self.forma = nueva_forma

    def set_unison(self, num_voces):
        self.unison = max(1, int(num_voces))

    def set_detune(self, cents):
        self.detune_cents = cents

    def generar(self, duracion):
        """
        Genera forma de onda con duración especificada.
        
        Si unison > 1, genera múltiples voces desafinadas y las mezcla.
        
        Args:
            duracion: Duración en segundos
            
        Returns:
            ndarray: Muestras de audio normalizadas
        """
        n_muestras = int(self.sample_rate * duracion)
        t = np.linspace(0, duracion, n_muestras, endpoint=False)

        if self.unison == 1:
            freq_detuned = self.frecuencia * (2 ** (self.detune_cents / 1200.0))
            return self._generar_forma(t, freq_detuned, self.fase)
        else:
            onda_total = np.zeros(n_muestras)
            detune_range = self.detune_cents
            for i in range(self.unison):
                detune_offset = (i / (self.unison - 1) - 0.5) * 2 * detune_range if self.unison > 1 else 0
                freq_voice = self.frecuencia * (2 ** (detune_offset / 1200.0))
                onda_total += self._generar_forma(t, freq_voice, self.fase)
            return onda_total / self.unison

    def _generar_forma(self, t, freq, fase):
        """Genera la forma de onda para una frecuencia y fase dadas."""
        if self.forma == 'sinusoidal':
            return self.amplitud * np.sin(2 * np.pi * freq * t + fase)
        elif self.forma == 'cuadrada':
            return self.amplitud * np.sign(np.sin(2 * np.pi * freq * t + fase))
        elif self.forma == 'triangular':
            return self.amplitud * (2 / np.pi) * np.arcsin(np.sin(2 * np.pi * freq * t + fase))
        elif self.forma == 'sierra':
            return self.amplitud * 2 * (freq * t + fase / (2 * np.pi) - np.floor(freq * t + fase / (2 * np.pi) + 0.5))
        else:
            return np.zeros_like(t)


# Ejemplo de uso (para pruebas):
if __name__ == "__main__":
    osc1 = Oscilador(frecuencia=440, forma='sinusoidal')
    osc2 = Oscilador(frecuencia=440, forma='sierra', amplitud=0.5)
    onda1 = osc1.generar(1.0)
    onda2 = osc2.generar(1.0)
    print("Onda generada y mezclada correctamente.")