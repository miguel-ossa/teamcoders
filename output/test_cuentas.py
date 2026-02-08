from datetime import datetime
from typing import Dict, List, Optional, Union
import unittest


class Movimiento:
    def __init__(self, tipo: str, monto: float, symbol: Optional[str] = None, cantidad: Optional[int] = None):
        self.tipo = tipo
        self.monto = monto
        self.symbol = symbol
        self.cantidad = cantidad
        self.timestamp = datetime.now()


class Cuenta:
    def __init__(self, id_cuenta: Union[str, int], deposito_inicial: float = 0.0):
        if deposito_inicial < 0:
            raise ValueError("El depósito inicial no puede ser negativo")
        
        self._id = id_cuenta
        self._balance = deposito_inicial
        self._acciones: Dict[str, int] = {}
        self._deposito_inicial = deposito_inicial
        self._historial: List[Movimiento] = []
        
        if deposito_inicial > 0:
            movimiento = Movimiento("DEPOSITO", deposito_inicial)
            self._historial.append(movimiento)

    def depositar(self, monto: float) -> None:
        if monto <= 0:
            raise ValueError("El monto a depositar debe ser positivo")
        
        self._balance += monto
        movimiento = Movimiento("DEPOSITO", monto)
        self._historial.append(movimiento)

    def retirar(self, monto: float) -> None:
        if monto <= 0:
            raise ValueError("El monto a retirar debe ser positivo")
        if monto > self._balance:
            raise ValueError("Fondos insuficientes para el retiro")
        
        self._balance -= monto
        movimiento = Movimiento("RETIRO", -monto)
        self._historial.append(movimiento)

    def comprar(self, symbol: str, cantidad: int) -> None:
        if cantidad <= 0:
            raise ValueError("La cantidad a comprar debe ser positiva")
        
        precio = get_share_pryce(symbol)
        costo_total = precio * cantidad
        
        if self._balance < costo_total:
            raise ValueError("Fondos insuficientes para comprar las acciones")
        
        self._balance -= costo_total
        
        if symbol in self._acciones:
            self._acciones[symbol] += cantidad
        else:
            self._acciones[symbol] = cantidad
        
        movimiento = Movimiento("COMPRA", -costo_total, symbol=symbol, cantidad=cantidad)
        self._historial.append(movimiento)

    def vender(self, symbol: str, cantidad: int) -> None:
        if cantidad <= 0:
            raise ValueError("La cantidad a vender debe ser positiva")
        
        if symbol not in self._acciones:
            raise ValueError(f"No posee acciones de {symbol}")
        
        if self._acciones[symbol] < cantidad:
            raise ValueError(f"No posee suficientes acciones de {symbol}")
        
        precio = get_share_pryce(symbol)
        ingreso = precio * cantidad
        
        self._acciones[symbol] -= cantidad
        
        if self._acciones[symbol] == 0:
            del self._acciones[symbol]
        
        self._balance += ingreso
        
        movimiento = Movimiento("VENTA", ingreso, symbol=symbol, cantidad=cantidad)
        self._historial.append(movimiento)

    def valor_portafolio(self) -> float:
        valor_acciones = sum(get_share_pryce(s) * q for s, q in self._acciones.items())
        return self._balance + valor_acciones

    def ganancia_perdida(self) -> float:
        return self.valor_portafolio() - self._deposito_inicial

    def tenencias(self) -> Dict[str, int]:
        return self._acciones.copy()

    def historial_transacciones(self) -> List[Movimiento]:
        return self._historial.copy()

    def balance_disponible(self) -> float:
        return self._balance


def get_share_pryce(symbol: str) -> float:
    precios = {
        "AAPL": 150.0,
        "TSLA": 240.0,
        "GOOGL": 2800.0
    }
    return precios.get(symbol, 100.0)


class TestCuenta(unittest.TestCase):
    
    def test_creacion_cuenta_con_deposito_inicial(self):
        cuenta = Cuenta("123", 1000.0)
        self.assertEqual(cuenta.balance_disponible(), 1000.0)
        self.assertEqual(cuenta.ganancia_perdida(), 0.0)
        self.assertEqual(len(cuenta.historial_transacciones()), 1)
        self.assertEqual(cuenta.historial_transacciones()[0].tipo, "DEPOSITO")
        self.assertEqual(cuenta.historial_transacciones()[0].monto, 1000.0)
    
    def test_creacion_cuenta_sin_deposito_inicial(self):
        cuenta = Cuenta("456")
        self.assertEqual(cuenta.balance_disponible(), 0.0)
        self.assertEqual(len(cuenta.historial_transacciones()), 0)
    
    def test_creacion_cuenta_con_deposito_negativo(self):
        with self.assertRaises(ValueError):
            Cuenta("789", -500.0)
    
    def test_depositar(self):
        cuenta = Cuenta("111", 500.0)
        cuenta.depositar(200.0)
        self.assertEqual(cuenta.balance_disponible(), 700.0)
        self.assertEqual(len(cuenta.historial_transacciones()), 2)
        self.assertEqual(cuenta.historial_transacciones()[-1].tipo, "DEPOSITO")
        self.assertEqual(cuenta.historial_transacciones()[-1].monto, 200.0)
    
    def test_depositar_monto_cero_o_negativo(self):
        cuenta = Cuenta("222", 500.0)
        with self.assertRaises(ValueError):
            cuenta.depositar(0)
        with self.assertRaises(ValueError):
            cuenta.depositar(-100.0)
    
    def test_retirar(self):
        cuenta = Cuenta("333", 1000.0)
        cuenta.retirar(300.0)
        self.assertEqual(cuenta.balance_disponible(), 700.0)
        self.assertEqual(len(cuenta.historial_transacciones()), 2)
        self.assertEqual(cuenta.historial_transacciones()[-1].tipo, "RETIRO")
        self.assertEqual(cuenta.historial_transacciones()[-1].monto, -300.0)
    
    def test_retirar_monto_cero_o_negativo(self):
        cuenta = Cuenta("444", 1000.0)
        with self.assertRaises(ValueError):
            cuenta.retirar(0)
        with self.assertRaises(ValueError):
            cuenta.retirar(-50.0)
    
    def test_retirar_fondos_insuficientes(self):
        cuenta = Cuenta("555", 100.0)
        with self.assertRaises(ValueError):
            cuenta.retirar(200.0)
    
    def test_comprar_acciones(self):
        cuenta = Cuenta("666", 5000.0)
        cuenta.comprar("AAPL", 10)
        self.assertEqual(cuenta.balance_disponible(), 3500.0)
        self.assertEqual(cuenta.tenencias(), {"AAPL": 10})
        self.assertEqual(len(cuenta.historial_transacciones()), 2)
        self.assertEqual(cuenta.historial_transacciones()[-1].tipo, "COMPRA")
        self.assertEqual(cuenta.historial_transacciones()[-1].symbol, "AAPL")
        self.assertEqual(cuenta.historial_transacciones()[-1].cantidad, 10)
        self.assertEqual(cuenta.historial_transacciones()[-1].monto, -1500.0)
    
    def test_comprar_acciones_monto_cero_o_negativo(self):
        cuenta = Cuenta("777", 5000.0)
        with self.assertRaises(ValueError):
            cuenta.comprar("AAPL", 0)
        with self.assertRaises(ValueError):
            cuenta.comprar("AAPL", -5)
    
    def test_comprar_acciones_fondos_insuficientes(self):
        cuenta = Cuenta("888", 500.0)
        with self.assertRaises(ValueError):
            cuenta.comprar("AAPL", 10)
    
    def test_vender_acciones(self):
        cuenta = Cuenta("999", 5000.0)
        cuenta.comprar("AAPL", 10)
        cuenta.vender("AAPL", 5)
        self.assertEqual(cuenta.balance_disponible(), 4250.0)
        self.assertEqual(cuenta.tenencias(), {"AAPL": 5})
        self.assertEqual(len(cuenta.historial_transacciones()), 3)
        self.assertEqual(cuenta.historial_transacciones()[-1].tipo, "VENTA")
        self.assertEqual(cuenta.historial_transacciones()[-1].symbol, "AAPL")
        self.assertEqual(cuenta.historial_transacciones()[-1].cantidad, 5)
        self.assertEqual(cuenta.historial_transacciones()[-1].monto, 750.0)
    
    def test_vender_acciones_no_posee(self):
        cuenta = Cuenta("AAA", 5000.0)
        with self.assertRaises(ValueError):
            cuenta.vender("AAPL", 1)
    
    def test_vender_acciones_cantidad_insuficiente(self):
        cuenta = Cuenta("BBB", 5000.0)
        cuenta.comprar("AAPL", 5)
        with self.assertRaises(ValueError):
            cuenta.vender("AAPL", 10)
    
    def test_vender_todas_las_acciones_de_una_empresa(self):
        cuenta = Cuenta("CCC", 5000.0)
        cuenta.comprar("AAPL", 5)
        cuenta.vender("AAPL", 5)
        self.assertEqual(cuenta.tenencias(), {})
        self.assertEqual(cuenta.balance_disponible(), 5000.0)
    
    def test_comprar_y_vender_multiples_acciones(self):
        cuenta = Cuenta("DDD", 10000.0)
        cuenta.comprar("AAPL", 5)
        cuenta.comprar("TSLA", 2)
        cuenta.comprar("GOOGL", 1)
        self.assertEqual(cuenta.balance_disponible(), 10000 - 750 - 480 - 2800)
        self.assertEqual(cuenta.tenencias(), {"AAPL": 5, "TSLA": 2, "GOOGL": 1})
        
        cuenta.vender("AAPL", 2)
        self.assertEqual(cuenta.balance_disponible(), 5970 + 300)
        self.assertEqual(cuenta.tenencias(), {"AAPL": 3, "TSLA": 2, "GOOGL": 1})
    
    def test_valor_portafolio(self):
        cuenta = Cuenta("EEE", 10000.0)
        cuenta.comprar("AAPL", 10)
        self.assertEqual(cuenta.valor_portafolio(), 10000)
    
    def test_ganancia_perdida(self):
        cuenta = Cuenta("FFF", 5000.0)
        self.assertEqual(cuenta.ganancia_perdida(), 0.0)
        cuenta.comprar("AAPL", 10)
        self.assertEqual(cuenta.ganancia_perdida(), 0.0)
    
    def test_historial_transacciones(self):
        cuenta = Cuenta("GGG", 1000.0)
        cuenta.depositar(500.0)
        cuenta.retirar(200.0)
        historial = cuenta.historial_transacciones()
        self.assertEqual(len(historial), 3)
        self.assertEqual(historial[0].tipo, "DEPOSITO")
        self.assertEqual(historial[1].tipo, "DEPOSITO")
        self.assertEqual(historial[2].tipo, "RETIRO")
    
    def test_tenencias_copia(self):
        cuenta = Cuenta("HHH", 5000.0)
        cuenta.comprar("AAPL", 10)
        tenencias = cuenta.tenencias()
        self.assertEqual(tenencias, {"AAPL": 10})
        tenencias["AAPL"] = 0
        self.assertEqual(cuenta.tenencias(), {"AAPL": 10})
    
    def test_id_cuenta(self):
        cuenta = Cuenta("ID123", 1000.0)
        self.assertEqual(cuenta._id, "ID123")
        cuenta2 = Cuenta(456, 1000.0)
        self.assertEqual(cuenta2._id, 456)


if __name__ == '__main__':
    unittest.main()