import unittest
from cuentas import Cuenta
from unittest.mock import patch

class TestCuenta(unittest.TestCase):
    def setUp(self):
        self.cuenta = Cuenta("usuario_prueba", 1000.0)
    
    @patch('cuentas.get_share_price', return_value=10.0)
    def test_comprar_acciones_valido(self, mock_get_price):
        self.cuenta.comprar_acciones("AAPL", 50)
        self.assertEqual(self.cuenta.saldo, 500.0)
        self.assertEqual(self.cuenta.tenencias["AAPL"], 50)
        self.assertEqual(len(self.cuenta.transacciones), 1)
        transaccion = self.cuenta.transacciones[0]
        self.assertEqual(transaccion["tipo"], "compra")
        self.assertEqual(transaccion["simbolo"], "AAPL")
        self.assertEqual(transaccion["cantidad"], 50)
        self.assertEqual(transaccion["precio"], 10.0)
    
    def test_comprar_acciones_saldo_insuficiente(self):
        cuenta = Cuenta("usuario_prueba", 100.0)
        with self.assertRaises(ValueError):
            cuenta.comprar_acciones("AAPL", 20)
    
    def test_retirar_saldo_negativo(self):
        with self.assertRaises(ValueError):
            self.cuenta.retirar(1500)
    
    def test_depositar_monto_negativo(self):
        with self.assertRaises(ValueError):
            self.cuenta.depositar(-100)
    
    def test_vender_acciones_no_disponibles(self):
        with self.assertRaises(ValueError):
            self.cuenta.vender_acciones("AAPL", 1)
    
    def test_calcular_valor_total(self):
        self.cuenta.saldo = 500.0
        self.cuenta.tenencias = {"AAPL": 50}
        with patch('cuentas.get_share_price', return_value=10.0):
            valor_total = self.cuenta.calcular_valor_total()
            self.assertEqual(valor_total, 1000.0)
    
    def test_calcular_ganancias_perdidas(self):
        self.cuenta.saldo = 1500.0
        self.assertEqual(self.cuenta.calcular_ganancias_perdidas(), 500.0)
    
    def test_obtener_tenencias(self):
        self.cuenta.tenencias = {"AAPL": 50}
        self.assertEqual(self.cuenta.obtener_tenencias(), {"AAPL": 50})
    
    def test_listar_transacciones(self):
        self.cuenta.depositar(200)
        self.cuenta.retirar(100)
        self.assertEqual(len(self.cuenta.listar_transacciones()), 2)

if __name__ == '__main__':
    unittest.main()

# Ejecución de tests
import test_cuentas
test_cuentas.TestCuenta().test_comprar_acciones_valido()
test_cuentas.TestCuenta().test_comprar_acciones_saldo_insuficiente()
test_cuentas.TestCuenta().test_retirar_saldo_negativo()
test_cuentas.TestCuenta().test_depositar_monto_negativo()
test_cuentas.TestCuenta().test_vender_acciones_no_disponibles()
test_cuentas.TestCuenta().test_calcular_valor_total()
test_cuentas.TestCuenta().test_calcular_ganancias_perdidas()
test_cuentas.TestCuenta().test_obtener_tenencias()
test_cuentas.TestCuenta().test_listar_transacciones()