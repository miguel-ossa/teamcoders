import unittest
from datetime import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '')))

from cuentas import Cuenta, get_share_price

class TestCuenta(unittest.TestCase):
    def setUp(self):
        self.cuenta = Cuenta()

    def test_depositar_aumenta_saldo_y_deposito_inicial(self):
        self.cuenta.depositar(1000)
        self.assertEqual(self.cuenta._saldo_efectivo, 1000)
        self.assertEqual(self.cuenta._deposito_inicial, 1000)

    def test_depositar_monto_negativo_o_cero_lanza(self):
        with self.assertRaises(ValueError):
            self.cuenta.depositar(0)
        with self.assertRaises(ValueError):
            self.cuenta.depositar(-10)

    def test_retirar_disminuye_saldo(self):
        self.cuenta.depositar(1000)
        self.cuenta.retirar(500)
        self.assertEqual(self.cuenta._saldo_efectivo, 500)

    def test_retirar_monto_negativo_o_cero_lanza(self):
        with self.assertRaises(ValueError):
            self.cuenta.retirar(0)
        with self.assertRaises(ValueError):
            self.cuenta.retirar(-10)

    def test_retirar_monto_mayor_que_saldo_lanza(self):
        self.cuenta.depositar(100)
        with self.assertRaises(ValueError):
            self.cuenta.retirar(150)

    def test_comprar_acciones_actualiza_tenencias_y_saldo(self):
        self.cuenta.depositar(20000)
        self.cuenta.comprar_acciones("AAPL", 10)
        self.assertEqual(self.cuenta._tenencias["AAPL"], 10)
        self.assertEqual(self.cuenta._saldo_efectivo, 20000 - 150.0 * 10)

    def test_comprar_acciones_cantidad_invalida_lanza(self):
        with self.assertRaises(ValueError):
            self.cuenta.comprar_acciones("AAPL", 0)
        with self.assertRaises(ValueError):
            self.cuenta.comprar_acciones("AAPL", -5)

    def test_comprar_acciones_fondos_insuficientes_lanza(self):
        self.cuenta.depositar(100)
        with self.assertRaises(ValueError):
            self.cuenta.comprar_acciones("TSLA", 1)  # TSLA 700 > 100

    def test_vender_acciones_actualiza_tenencias_y_saldo(self):
        self.cuenta.depositar(20000)
        self.cuenta.comprar_acciones("AAPL", 10)
        self.cuenta.vender_acciones("AAPL", 5)
        self.assertEqual(self.cuenta._tenencias["AAPL"], 5)
        self.assertAlmostEqual(self.cuenta._saldo_efectivo, (20000 - 150*10) + 150*5)

    def test_vender_acciones_cantidad_invalida_lanza(self):
        with self.assertRaises(ValueError):
            self.cuenta.vender_acciones("AAPL", 0)
        with self.assertRaises(ValueError):
            self.cuenta.vender_acciones("AAPL", -3)

    def test_vender_acciones_no_suficientes_lanza(self):
        self.cuenta.depositar(1000)
        with self.assertRaises(ValueError):
            self.cuenta.vender_acciones("AAPL", 1)

    def test_vender_acciones_elimina_tenencia_cuando_cantidad_llega_a_cero(self):
        self.cuenta.depositar(20000)
        self.cuenta.comprar_acciones("AAPL", 10)
        self.cuenta.vender_acciones("AAPL", 10)
        self.assertNotIn("AAPL", self.cuenta._tenencias)

    def test_obtener_tenencias(self):
        self.cuenta.depositar(20000)
        self.cuenta.comprar_acciones("AAPL", 5)
        self.assertEqual(self.cuenta.obtener_tenencias(), {"AAPL": 5})

    def test_valor_portafolio_calcula_correcto(self):
        self.cuenta.depositar(1000)
        self.assertAlmostEqual(self.cuenta.valor_portafolio(), 1000)
        self.cuenta.comprar_acciones("AAPL", 5)  # 5*150=750
        self.assertAlmostEqual(self.cuenta.valor_portafolio(), 1000 - 750 + 750)

    def test_ganancias_perdidas_calcula_correcto(self):
        self.cuenta.depositar(1000)
        self.assertAlmostEqual(self.cuenta.ganancias_perdidas(), 0)
        self.cuenta.comprar_acciones("AAPL", 5)
        self.assertAlmostEqual(self.cuenta.ganancias_perdidas(), self.cuenta.valor_portafolio() - 1000)

    def test_listar_transacciones_registra_correctamente(self):
        self.cuenta.depositar(1000)
        self.cuenta.retirar(500)
        self.cuenta.comprar_acciones("AAPL", 2)
        self.cuenta.vender_acciones("AAPL", 1)
        transacciones = self.cuenta.listar_transacciones()
        self.assertEqual(len(transacciones), 4)
        tipos = [t["tipo"] for t in transacciones]
        self.assertEqual(tipos, ["deposito", "retiro", "compra", "venta"])


if __name__ == "__main__":
    unittest.main()