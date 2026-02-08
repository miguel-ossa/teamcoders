import uuid
import time
from copy import deepcopy


def get_share_pryce(symbol: str) -> float:
    """Devuelve el precio simulado de una acción según su símbolo."""
    precios_fijos = {
        "AAPL": 150.0,
        "TSLA": 250.0,
        "GOOGL": 140.0
    }
    symbol_upper = symbol.upper()
    if symbol_upper in precios_fijos:
        return precios_fijos[symbol_upper]
    raise ValueError("Símbolo no soportado")


class Cuenta:
    def __init__(self) -> None:
        self.id_cuenta = str(uuid.uuid4())
        self.saldo = 0.0
        self.deposito_inicial = 0.0
        self.acciones = {}
        self.historial = []

    def depositar(self, monto: float) -> float:
        if monto <= 0:
            raise ValueError("El monto debe ser mayor que cero.")
        
        self.saldo += monto
        if self.deposito_inicial == 0:
            self.deposito_inicial = monto
        
        self._registrar_transaccion("DEPOSITO", {"monto": monto, "nuevo_saldo": self.saldo})
        return self.saldo

    def retirar(self, monto: float) -> float:
        if monto <= 0:
            raise ValueError("El monto debe ser mayor que cero.")
        if self.saldo - monto < 0:
            raise ValueError("Fondos insuficientes para realizar el retiro.")
        
        self.saldo -= monto
        self._registrar_transaccion("RETIRO", {"monto": monto, "nuevo_saldo": self.saldo})
        return self.saldo

    def comprar_accion(self, simbolo: str, cantidad: int) -> dict:
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")
        if not isinstance(simbolo, str) or not simbolo.strip():
            raise ValueError("El símbolo debe ser una cadena no vacía.")
        
        try:
            precio_unitario = get_share_pryce(simbolo)
        except ValueError:
            raise
        
        costo_total = precio_unitario * cantidad
        if self.saldo < costo_total:
            raise ValueError("Fondos insuficientes para completar la compra.")
        
        self.saldo -= costo_total
        if simbolo in self.acciones:
            self.acciones[simbolo] += cantidad
        else:
            self.acciones[simbolo] = cantidad
        
        detalle = {
            "simbolo": simbolo,
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "costo_total": costo_total,
            "nuevo_saldo": self.saldo
        }
        self._registrar_transaccion("COMPRA", detalle)
        
        return detalle

    def vender_accion(self, simbolo: str, cantidad: int) -> dict:
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")
        if simbolo not in self.acciones:
            raise ValueError(f"No posee acciones de {simbolo}.")
        if self.acciones[simbolo] < cantidad:
            raise ValueError("Cantidad insuficiente de acciones para vender.")
        
        try:
            precio_unitario = get_share_pryce(simbolo)
        except ValueError:
            raise
        
        ingreso_total = precio_unitario * cantidad
        self.saldo += ingreso_total
        self.acciones[simbolo] -= cantidad
        
        if self.acciones[simbolo] == 0:
            del self.acciones[simbolo]
        
        detalle = {
            "simbolo": simbolo,
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "ingreso_total": ingreso_total,
            "nuevo_saldo": self.saldo
        }
        self._registrar_transaccion("VENTA", detalle)
        
        return detalle

    def valor_portafolio(self) -> float:
        valor_acciones = sum(get_share_pryce(s) * q for s, q in self.acciones.items())
        return self.saldo + valor_acciones

    def ganancia_perdida(self) -> float:
        return self.valor_portafolio() - self.deposito_inicial

    def tenencias(self) -> dict:
        return deepcopy(self.acciones)

    def transacciones(self) -> list:
        return deepcopy(self.historial)

    def _registrar_transaccion(self, tipo: str, detalle: dict) -> None:
        transaccion = {
            "tipo": tipo,
            "timestamp": time.time(),
            "detalle": detalle
        }
        self.historial.append(transaccion)