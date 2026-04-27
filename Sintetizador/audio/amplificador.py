import numpy as np

class Mezclador:
    """
    Mezclador de audio para combinar señales de audio.
    
    Permite que se controle el nivel de amplificación de cada señal individualmente
    antes de combinarlas.
    """

    def __init__(self, nivel_osc1=1.0, nivel_osc2=1.0):
        self.nivel_osc1 = nivel_osc1
        self.nivel_osc2 = nivel_osc2

    def set_nivel_osc1(self, nivel):
        self.nivel_osc1 = max(0.0, float(nivel))

    def set_nivel_osc2(self, nivel):
        self.nivel_osc2 = max(0.0, float(nivel))
    
    def mezclar(self, señal1, señal2):
        """
        Mezcla dos señales de audio aplicando los niveles de amplificación independientes.
        """
        if señal1 is None and señal2 is None:
            return np.array([])
        
        if señal1 is None:
            return self.nivel_osc2 * señal2
        
        if señal2 is None:
            return self.nivel_osc1 * señal1
        
        longitud = min(len(señal1), len(señal2))
        señal1 = señal1[:longitud]
        señal2 = señal2[:longitud]
        return (señal1 * self.nivel_osc1) + (señal2 * self.nivel_osc2)
    
class Amplificador:
    """
    Controla la ganancia, el volumen y la protección contra clipping
    """
    def __init__(self, ganancia=1.0, master = 0.8, saturacion = False, normalizar= True):
        self.ganancia = float(ganancia)
        self.master = float(master)
        self.saturacion = bool(saturacion)
        self.normalizar = bool(normalizar)

    def set_ganancia(self, ganancia):
        self.ganancia = max(0.0, float(ganancia))

    def set_master(self, master):
        self.master = max(0.0, min(1.0, float(master)))
        
    def set_saturacion(self, saturacion):
        self.saturacion = bool(saturacion)
        
    def set_normalizar(self, normalizar):
        self.normalizar = bool(normalizar)
        
    def amplificar(self, señal):
        """
        Se aplica la amplificación a la señal de audio
        """

        if señal is None or len(señal) == 0:
            return señal
            
        salida = señal.astype(float).copy()

        salida = salida * self.ganancia     #ganancia principal

        if self.saturacion:
            salida = np.tanh(salida)        #opcional saturación soft clipping

        if self.normalizar:
            salida = self.normalizar_si_clipea(salida) #opcional normalización para evitar clipping

        salida = salida * self.master      #volumen final

        return salida
        
    def normalizar_si_clipea(self, señal):
        """
        Normaliza la señal si detecta que los valores salen fuera del rango [-1, 1]
        """
        max_val = np.max(np.abs(señal))

        if max_val > 1.0:
            return señal / max_val
            
        return señal