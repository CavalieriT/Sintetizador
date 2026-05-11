import unittest
import numpy as np

from audio.amplificador import Mezclador, Amplificador


class TestMezclador(unittest.TestCase):

    def test_mezcla_dos_senales_con_niveles(self):
        mezclador = Mezclador(nivel_osc1=0.5, nivel_osc2=2.0)

        senal1 = np.array([1.0, -1.0, 0.25])
        senal2 = np.array([0.5, 0.5, -0.5])

        resultado = mezclador.mezclar(senal1, senal2)

        esperado = np.array([1.5, 0.5, -0.875])
        np.testing.assert_allclose(resultado, esperado)

    def test_mezcla_usa_longitud_mas_corta(self):
        mezclador = Mezclador()

        senal1 = np.array([1.0, 2.0, 3.0])
        senal2 = np.array([10.0, 20.0])

        resultado = mezclador.mezclar(senal1, senal2)

        esperado = np.array([11.0, 22.0])
        np.testing.assert_allclose(resultado, esperado)

    def test_mezcla_con_senales_none(self):
        mezclador = Mezclador(nivel_osc1=0.25, nivel_osc2=0.5)

        senal = np.array([1.0, -1.0])

        np.testing.assert_allclose(
            mezclador.mezclar(None, senal),
            np.array([0.5, -0.5])
        )

        np.testing.assert_allclose(
            mezclador.mezclar(senal, None),
            np.array([0.25, -0.25])
        )

        self.assertEqual(mezclador.mezclar(None, None).size, 0)


class TestAmplificador(unittest.TestCase):

    def test_aplica_ganancia_y_master_sin_normalizar(self):
        amplificador = Amplificador(
            ganancia=2.0,
            master=0.25,
            normalizar=False
        )

        senal = np.array([0.5, -0.5, 0.25])

        resultado = amplificador.amplificar(senal)

        esperado = np.array([0.25, -0.25, 0.125])
        np.testing.assert_allclose(resultado, esperado)

    def test_normaliza_si_clipea(self):
        amplificador = Amplificador(
            ganancia=2.0,
            master=0.5,
            normalizar=True
        )

        senal = np.array([0.5, -2.0])

        resultado = amplificador.amplificar(senal)

        esperado = np.array([0.125, -0.5])
        np.testing.assert_allclose(resultado, esperado)
        self.assertLessEqual(np.max(np.abs(resultado)), 0.5)

    def test_saturacion_soft_clipping(self):
        amplificador = Amplificador(
            ganancia=3.0,
            master=1.0,
            saturacion=True,
            normalizar=False
        )

        senal = np.array([-1.0, 0.0, 1.0])

        resultado = amplificador.amplificar(senal)

        esperado = np.tanh(senal * 3.0)
        np.testing.assert_allclose(resultado, esperado)

    def test_senal_vacia_o_none_no_falla(self):
        amplificador = Amplificador()

        self.assertIsNone(amplificador.amplificar(None))
        self.assertEqual(amplificador.amplificar(np.array([])).size, 0)


if __name__ == "__main__":
    unittest.main()
