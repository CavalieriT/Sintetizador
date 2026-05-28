import numpy as np

class Filtro:
    """
    Filtro de audio básico para procesamiento de señales de audio.
    
    Parámetros:
    -tipo: "lowpass" o paso bajo, "highpass" o paso alto, "bandpass" o pasabanda
    -cutoff: frecuencia de corte (en Hz)
    -sample_rate: frecuencia de muestro de la señal
    -bandwidth: ancho de banda para filtros bandpass
    """

    def __init__(self, tipo='lowpass', cutoff=1000, sample_rate=44100, bandwidth=500):
        self.tipo = tipo
        self.cutoff = cutoff
        self.sample_rate = sample_rate
        self.bandwidth = bandwidth

    def set_tipo(self, tipo):
        self.tipo = tipo
    
    def set_cutoff(self, cutoff):
        self.cutoff = max(1, float(cutoff))
    
    def set_bandwidth(self, bandwidth):
        self.bandwidth = max(1, float(bandwidth))

    def aplicar(self, señal):
        """
        Aplica el filtro seleccionado a una señal de audio.
        
        Parámetro:
            señal: array NumPy con muestras de audio
            
        Devuelve:
            un array NumPy filtrado
        """

        if señal is None or len(señal) == 0:
            return señal
        
        if self.tipo == 'lowpass':
            return self._lowpass(señal, self.cutoff)
        
        elif self.tipo == 'highpass':
            return self._highpass(señal, self.cutoff)
        
        elif self.tipo == 'bandpass':
            lowcut = max(1, self.cutoff - self.bandwidth / 2)
            highcut = self.cutoff + self.bandwidth / 2
            return self._bandpass(señal, lowcut, highcut)
        
        return señal
    
    def _lowpass(self, señal, cutoff):
        """
        Aplica filtro paso bajo a la señal.
        """
        alpha = self._calcula_alpha_lowpass(cutoff)
        output = np.zeros_like(señal)

        output[0] = señal[0]
        for n in range(1, len(señal)):
            output[n] = output[n-1] + alpha * (señal[n] - output[n-1])

        return output
    
    def _highpass(self, señal, cutoff):
        """
        Aplica filtro paso alto a la señal.
        """
        alpha = self._calcula_alpha_highpass(cutoff)
        output = np.zeros_like(señal)

        output[0] = 0
        for n in range(1, len(señal)):
            output[n] = alpha * (output[n-1] + señal[n] - señal[n-1])

        return output
    
    def _bandpass(self, señal, lowcut, highcut):
        """
        Aplica filtro pasabanda IIR de segundo orden de tipo biquad a la señal.
        """
        if señal is None or len(señal) == 0:
            return señal

        fc = (lowcut + highcut) / 2
        bandwidth = highcut - lowcut

        q = fc / bandwidth if bandwidth > 0 else 1.0
        q = max(0.1, q)

        w0 = 2 * np.pi * fc / self.sample_rate
        alpha = np.sin(w0) / (2 * q)

        b0 = alpha
        b1 = 0
        b2 = -alpha
        a0 = 1 + alpha
        a1 = -2 * np.cos(w0)
        a2 = 1 - alpha

        b0 /= a0
        b1 /= a0
        b2 /= a0
        a1 /= a0
        a2 /= a0

        output = np.zeros_like(señal, dtype=float)

        x1 = x2 = 0.0
        y1 = y2 = 0.0

        for n in range(len(señal)):
            x0 = señal[n]
            y0 = b0 * x0 + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2

            output[n] = y0

            x2 = x1
            x1 = x0
            y2 = y1
            y1 = y0

        return output
    
    def _calcula_alpha_lowpass(self, cutoff):
        """
        Calcula el coeficiente alpha del filtro
        
        Mientras mayor sea el cutoff, más rápido responderá el filtro a los cambios en la señal.
        """

        dt = 1 / self.sample_rate #dt = tiempo entre muestras
        rc = 1 / (2 * np.pi * cutoff) #rc = el tiempo de respuesta del filtro, representa la constante de tiempo del filtro
                                      #que determina la rapidez con la que el filtro responde a los cambios en la señal.
        alpha = dt / (rc + dt)
        return alpha
    
    def _calcula_alpha_highpass(self, cutoff):
        """
        Calcula el coeficiente alpha del filtro
        
        Mientras mayor sea el cutoff, más rápido responderá el filtro a los cambios en la señal.
        """

        dt = 1 / self.sample_rate
        rc = 1 / (2 * np.pi * cutoff)
        alpha = rc / (rc + dt)
        return alpha