```python
import unittest
from cuentas import Cuenta, get_share_price

class TestCuenta(unittest.TestCase):
    def test_init_valid_deposit(self):
        cuenta = Cuenta(1000)
        self.assertEqual(cuenta.saldo, 1000)
        self.assertEqual(cuenta.portafolio, {})
        self.assertEqual(cuenta.transacciones, [])

    def test_init_invalid_deposit(self):
        with self.assertRaises(ValueError):
            Cuenta(0)
        with self.assertRaises(ValueError):
            Cuenta(-100)

    def test_depositar_valid(self):
        cuenta = Cuenta(1000)
        cuenta.depositar(500)
        self.assertEqual(cuenta.saldo, 1500)
        self.assertEqual(cuenta.transacciones[-1], {'tipo': 'deposito', 'monto': 500})

    def test_depositar_invalid(self):
        cuenta = Cuenta(1000)
        with self.assertRaises(ValueError):
            cuenta.depositar(0)
        with self.assertRaises(ValueError):
            cuenta.depositar(-100)

    def test_retirar_valid(self):
        cuenta = Cuenta(1000)
        cuenta.retirar(200)
        self.assertEqual(cuenta.saldo, 800)
        self.assertEqual(cuenta.transacciones[-1], {'tipo': 'retiro', 'monto': 200})

    def test_retirar_invalid(self):
        cuenta = Cuenta(1000)
        with self.assertRaises(ValueError):
            cuenta.retirar(0)
        with self.assertRaises(ValueError):
            cuenta.retirar(-100)
        with self.assertRaises(ValueError):
            cuenta.retirar(1200)

    def test_comprar_valid(self):
        cuenta = Cuenta(1000)
        cuenta.comprar("AAPL", 1)
        self.assertEqual(cuenta.saldo, 810.0)
        self.assertEqual(cuenta.portafolio, {"AAPL": 1})
        self.assertEqual(cuenta.transacciones[-1], {"tipo": "compra", "simbolo": "AAPL", "cantidad": 1, "monto": 190.0})

    def test_comprar_invalid(self):
        cuenta = Cuenta(1000)
        with self.assertRaises(ValueError):
            cuenta.comprar("", 1)
        with self.assertRaises(ValueError):
            cuenta.comprar("AAPL", 0)
        with self.assertRaises(ValueError):
            cuenta.comprar("AAPL", -1)
        with self.assertRaises(ValueError):
            cuenta.comprar("XYZ", 1)

    def test_vender_valid(self):
        cuenta = Cuenta(1000)
        cuenta.comprar("AAPL", 1)
        cuenta.vender("AAPL", 1)
        self.assertEqual(cuenta.saldo, 1000.0)
        self.assertEqual(cuenta.portafolio, {})
        self.assertEqual(cuenta.transacciones[-1], {"tipo": "venta", "simbolo": "AAPL", "cantidad": 1, "monto": 190.0})

    def test_vender_invalid(self):
        cuenta = Cuenta(1000)
        with self.assertRaises(ValueError):
            cuenta.vender("", 1)
        with self.assertRaises(ValueError):
            cuenta.vender("AAPL", 0)
        with self.assertRaises(ValueError):
            cuenta.vender("AAPL", -1)
        cuenta.comprar("AAPL", 1)
        with self.assertRaises(ValueError):
            cuenta.vender("AAPL", 2)

    def test_valor_total_portafolio(self):
        cuenta = Cuenta(1000)
        cuenta.comprar("AAPL", 1)
        cuenta.comprar("TSLA", 1)
        self.assertEqual(cuenta.valor_total_portafolio(), 450.0)

    def test_ganancias_o_perdidas(self):
        cuenta = Cuenta(1000)
        cuenta.comprar("AAPL", 1)
        self.assertEqual(cuenta.ganancias_o_perdidas(), -190.0)

    def test_obtener_tenencias(self):
        cuenta = Cuenta(1000)
        cuenta.comprar("AAPL", 1)
        self.assertEqual(cuenta.obtener_tenencias(), {"AAPL": 1})
        cuenta.obtener_tenencias()["AAPL"] = 0
        self.assertEqual(cuenta.portafolio, {"AAPL": 1})

    def test_obtener_transacciones(self):
        cuenta = Cuenta(1000)
        cuenta.depositar(500)
        cuenta.retirar(200)
        self.assertEqual(cuenta.obtener_transacciones(), [{"tipo": "deposito", "monto": 500}, {"tipo": "retiro", "monto": 200}])

if __name__ == "__main__":
    unittest.main()
```