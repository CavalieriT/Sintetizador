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
        
        Args:
            señal: array NumPy con muestras de audio
            
        Returns:
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
        Aplica filtro pasabanda a la señal. Primero highpass y luego lowpass.
        """

        dt = 1 / self.sample_rate

        rc_low = 1 / (2 * np.pi * lowcut)
        alpha_low = rc_low / (rc_low + dt)

        rc_high = 1 / (2 * np.pi * highcut)
        alpha_high = dt / (rc_high + dt)

        hp = np.zeros_like(señal)
        lp = np.zeros_like(señal)

        for n in range(1, len(señal)):
            hp[n] = alpha_low * (hp[n-1] + señal[n] - señal[n-1])

        lp[0] = hp[0]

        for n in range(1, len(señal)):
            lp[n] = lp[n-1] + alpha_high * (hp[n] - lp[n-1])

        return lp
    
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