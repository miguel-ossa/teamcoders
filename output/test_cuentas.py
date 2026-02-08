import unittest
from cuentas import Cuenta, get_share_price

class TestCuenta(unittest.TestCase):
    def setUp(self):
        self.cuenta = Cuenta(1000.0)
    
    def test_inicializacion(self):
        self.assertEqual(self.cuenta.saldo_actual, 1000.0)
        self.assertEqual(self.cuenta.saldo_inicial, 1000.0)
        self.assertEqual(self.cuenta.portafolio, {})
        self.assertEqual(self.cuenta.transacciones, [])
    
    def test_depositar(self):
        self.cuenta.depositar(500)
        self.assertEqual(self.cuenta.saldo_actual, 1500.0)
        self.assertEqual(len(self.cuenta.transacciones), 1)
        self.assertEqual(self.cuenta.transacciones[0]['tipo'], 'depósito')
    
    def test_retirar(self):
        self.cuenta.retirar(200)
        self.assertEqual(self.cuenta.saldo_actual, 800.0)
        self.assertEqual(len(self.cuenta.transacciones), 1)
        self.assertEqual(self.cuenta.transacciones[0]['tipo'], 'retiro')
    
    def test_comprar_acciones(self):
        self.cuenta.comprar_acciones('AAPL', 2)
        self.assertEqual(self.cuenta.saldo_actual, 1000.0 - 2*150.0)
        self.assertEqual(self.cuenta.portafolio, {'AAPL': 2})
        self.assertEqual(len(self.cuenta.transacciones), 1)
        self.assertEqual(self.cuenta.transacciones[0]['tipo'], 'compra')
    
    def test_vender_acciones(self):
        self.cuenta.comprar_acciones('AAPL', 2)
        self.cuenta.vender_acciones('AAPL', 1)
        self.assertEqual(self.cuenta.saldo_actual, 1000.0 - 2*150.0 + 1*150.0)
        self.assertEqual(self.cuenta.portafolio, {'AAPL': 1})
        self.assertEqual(len(self.cuenta.transacciones), 2)
        self.assertEqual(self.cuenta.transacciones[1]['tipo'], 'venta')
    
    def test_calcular_valor_total(self):
        self.cuenta.comprar_acciones('AAPL', 2)
        self.assertEqual(self.cuenta.calcular_valor_total(), 2*150.0)
    
    def test_calcular_ganancias_perdidas(self):
        self.cuenta.comprar_acciones('AAPL', 2)
        self.assertEqual(self.cuenta.calcular_ganancias_perdidas(), (2*150.0) - 1000.0)
    
    def test_get_tenencias(self):
        self.cuenta.comprar_acciones('AAPL', 2)
        self.assertEqual(self.cuenta.get_tenencias(), {'AAPL': 2})
    
    def test_listar_transacciones(self):
        self.cuenta.depositar(500)
        self.cuenta.retirar(200)
        transacciones = self.cuenta.listar_transacciones()
        self.assertEqual(len(transacciones), 2)
        self.assertEqual(transacciones[0]['tipo'], 'depósito')
        self.assertEqual(transacciones[1]['tipo'], 'retiro')
    
    def test_excepciones_inicializacion(self):
        with self.assertRaises(ValueError):
            Cuenta(0)
        with self.assertRaises(ValueError):
            Cuenta(-100)
        with self.assertRaises(ValueError):
            Cuenta('1000')
    
    def test_excepciones_depositar(self):
        with self.assertRaises(ValueError):
            self.cuenta.depositar(0)
        with self.assertRaises(ValueError):
            self.cuenta.depositar(-50)
        with self.assertRaises(ValueError):
            self.cuenta.depositar('500')
    
    def test_excepciones_retirar(self):
        with self.assertRaises(ValueError):
            self.cuenta.retirar(0)
        with self.assertRaises(ValueError):
            self.cuenta.retirar(-50)
        with self.assertRaises(ValueError):
            self.cuenta.retirar(2000)
        with self.assertRaises(ValueError):
            self.cuenta.retirar('500')
    
    def test_excepciones_comprar(self):
        with self.assertRaises(ValueError):
            self.cuenta.comprar_acciones('', 2)
        with self.assertRaises(ValueError):
            self.cuenta.comprar_acciones('AAPL', 0)
        with self.assertRaises(ValueError):
            self.cuenta.comprar_acciones('AAPL', -2)
        with self.assertRaises(ValueError):
            self.cuenta.comprar_acciones('AAPL', 2)
        with self.assertRaises(ValueError):
            self.cuenta.comprar_acciones('TSLA', 1000)
    
    def test_excepciones_vender(self):
        with self.assertRaises(ValueError):
            self.cuenta.vender_acciones('', 2)
        with self.assertRaises(ValueError):
            self.cuenta.vender_acciones('AAPL', 0)
        with self.assertRaises(ValueError):
            self.cuenta.vender_acciones('AAPL', -2)
        with self.assertRaises(ValueError):
            self.cuenta.vender_acciones('AAPL', 1)