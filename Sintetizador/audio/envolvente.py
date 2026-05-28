import numpy as np


class GeneradorEnvolvente:
    """
    Generador de envolventes.

    Tipos soportados:
    - gate: mantiene la señal activa durante toda la duración.
    - ad: attack y decay.
    - adsr: attack, decay, sustain y release.
    """

    def __init__(self, tipo="adsr", attack=0.05, decay=0.15, sustain=0.7, release=0.2, sample_rate=44100):
        self.tipo = tipo
        self.attack = float(attack)
        self.decay = float(decay)
        self.sustain = float(sustain)
        self.release = float(release)
        self.sample_rate = sample_rate

    def set_tipo(self, tipo):
        self.tipo = tipo

    def set_attack(self, attack):
        self.attack = max(0.001, float(attack))

    def set_decay(self, decay):
        self.decay = max(0.001, float(decay))

    def set_sustain(self, sustain):
        self.sustain = max(0.0, min(1.0, float(sustain)))

    def set_release(self, release):
        self.release = max(0.001, float(release))

    def generar(self, duracion):
        """
        Genera la curva de envolvente según el tipo seleccionado para la duración dada.
        """
        total_muestras = int(duracion * self.sample_rate)
        if total_muestras <= 0:
            return np.array([])

        if self.tipo == "gate":
            return self._gate(total_muestras)

        elif self.tipo == "ad":
            return self._ad(total_muestras)

        elif self.tipo == "adsr":
            return self._adsr(total_muestras)

        return np.ones(total_muestras)

    def aplicar(self, señal):
        """
        Aplica la envolvente multiplicando a la señal por la curva generada.
        """
        if señal is None or len(señal) == 0:
            return señal

        envolvente = self.generar(len(señal) / self.sample_rate)
        longitud = min(len(señal), len(envolvente))

        return señal[:longitud] * envolvente[:longitud]

    def _gate(self, total_muestras):
        """
        Envolvente Gate: mantiene la amplitud constante.
        """
        return np.ones(total_muestras)

    def _ad(self, total_muestras):
        """
        Envolvente AD: attack + decay hasta cero.
        """
        muestras_attack = int(self.attack * self.sample_rate)
        muestras_attack = max(1, min(muestras_attack, total_muestras))
        muestras_decay = total_muestras - muestras_attack
        muestras_decay = max(0, muestras_decay)

        attack = np.linspace(0.0, 1.0, muestras_attack)

        if muestras_decay > 0:
            decay = np.linspace(1.0, 0.0, muestras_decay)
            return np.concatenate([attack, decay])

        return attack[:total_muestras]

    def _adsr(self, total_muestras):
        """
        Envolvente ADSR: Attack, Decay, Sustain y Release.
        Si la duración es muy corta, se reducen proporcionalmente los segmentos.
        """
        muestras_attack = int(self.attack * self.sample_rate)
        muestras_decay = int(self.decay * self.sample_rate)
        muestras_release = int(self.release * self.sample_rate)
        muestras_attack = max(1, muestras_attack)
        muestras_decay = max(1, muestras_decay)
        muestras_release = max(1, muestras_release)

        muestras_sustain = total_muestras - muestras_attack - muestras_decay - muestras_release

        if muestras_sustain < 0:
            # si dura muy poco, se reescala.
            total = muestras_attack + muestras_decay + muestras_release

            factor = total_muestras / total
            muestras_attack = max(1, int(muestras_attack * factor))
            muestras_decay = max(1, int(muestras_decay * factor))
            muestras_release = max(1, total_muestras - muestras_attack - muestras_decay)
            muestras_sustain = 0

        attack = np.linspace(0.0, 1.0, muestras_attack)
        decay = np.linspace(1.0, self.sustain, muestras_decay)
        sustain = np.full(muestras_sustain, self.sustain)
        release = np.linspace(self.sustain, 0.0, muestras_release)

        envolvente = np.concatenate([attack,decay,sustain,release])

        return envolvente[:total_muestras]