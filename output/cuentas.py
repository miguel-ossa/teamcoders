from typing import Dict, List, Optional
from datetime import datetime


def get_share_price(symbol: str) -> float:
    """
    Función simulada para obtener el precio actual de una acción.
    Implementación de prueba incluye precios fijos para:
    - AAPL: 150.0
    - TSLA: 700.0
    - GOOGL: 2800.0

    Parámetros:
    - symbol: str, símbolo de la acción

    Retorna:
    - float: precio unitario actual de la acción

    Lanza excepción si símbolo no reconocido.
    """
    precios_fijos = {
        "AAPL": 150.0,
        "TSLA": 700.0,
        "GOOGL": 2800.0,
    }
    if symbol not in precios_fijos:
        raise ValueError(f"Símbolo no reconocido: {symbol}")
    return precios_fijos[symbol]


class Cuenta:
    def __init__(self):
        """
        Inicializa una cuenta vacía con saldo cero y sin tenencias.
        """
        self._saldo_efectivo: float = 0.0
        self._deposito_inicial: float = 0.0
        self._tenencias: Dict[str, int] = {}
        self._transacciones: List[Dict] = []

    def depositar(self, monto: float) -> None:
        """
        Deposita fondos en la cuenta, incrementando saldo efectivo y depósito inicial.
        Parámetros: 
            - monto: float, monto positivo a depositar
        Lanza excepción si monto <= 0.
        Registra la transacción.
        """
        if monto <= 0:
            raise ValueError("El monto a depositar debe ser positivo.")
        self._saldo_efectivo += monto
        self._deposito_inicial += monto
        self._registrar_transaccion("deposito", cantidad=monto)

    def retirar(self, monto: float) -> None:
        """
        Retira fondos del saldo efectivo.
        Parámetros:
            - monto: float, monto positivo a retirar
        Lanza excepción si monto <= 0 o si el retiro dejaría saldo negativo.
        Registra la transacción.
        """
        if monto <= 0:
            raise ValueError("El monto a retirar debe ser positivo.")
        if self._saldo_efectivo - monto < 0:
            raise ValueError("Fondos insuficientes para el retiro.")
        self._saldo_efectivo -= monto
        self._registrar_transaccion("retiro", cantidad=monto)

    def comprar_acciones(self, simbolo: str, cantidad: int) -> None:
        """
        Registra la compra de acciones.
        Parámetros:
            - simbolo: str, símbolo de la acción (ej. "AAPL")
            - cantidad: int, cantidad de acciones a comprar (> 0)
        Valida que el usuario tiene saldo efectivo suficiente para pagar la compra.
        Actualiza tenencias y saldo efectivo.
        Registra la transacción (incluye precio unitario actual).
        Lanza excepción en caso de fondos insuficientes o cantidad inválida.
        """
        if cantidad <= 0:
            raise ValueError("La cantidad de acciones a comprar debe ser mayor que cero.")
        precio_unitario = get_share_price(simbolo)
        costo_total = precio_unitario * cantidad
        if self._saldo_efectivo < costo_total:
            raise ValueError("Fondos insuficientes para comprar las acciones solicitadas.")
        self._saldo_efectivo -= costo_total
        self._tenencias[simbolo] = self._tenencias.get(simbolo, 0) + cantidad
        self._registrar_transaccion("compra", simbolo=simbolo, cantidad=cantidad, precio_unitario=precio_unitario)

    def vender_acciones(self, simbolo: str, cantidad: int) -> None:
        """
        Registra la venta de acciones.
        Parámetros:
            - simbolo: str, símbolo de la acción
            - cantidad: int, cantidad de acciones a vender (> 0)
        Valida que el usuario posee suficientes acciones.
        Aumenta el saldo efectivo según precio unitario actual * cantidad.
        Actualiza tenencias y saldo.
        Registra la transacción (incluye precio unitario actual).
        Lanza excepción si la cantidad inválida o acciones insuficientes.
        """
        if cantidad <= 0:
            raise ValueError("La cantidad de acciones a vender debe ser mayor que cero.")
        if simbolo not in self._tenencias or self._tenencias[simbolo] < cantidad:
            raise ValueError("No posee suficientes acciones para vender.")
        precio_unitario = get_share_price(simbolo)
        ingreso_total = precio_unitario * cantidad
        self._tenencias[simbolo] -= cantidad
        if self._tenencias[simbolo] == 0:
            del self._tenencias[simbolo]
        self._saldo_efectivo += ingreso_total
        self._registrar_transaccion("venta", simbolo=simbolo, cantidad=cantidad, precio_unitario=precio_unitario)

    def obtener_tenencias(self) -> Dict[str, int]:
        """
        Retorna un diccionario con las tenencias actuales (símbolo -> cantidad).
        """
        return dict(self._tenencias)

    def valor_portafolio(self) -> float:
        """
        Calcula y retorna el valor total del portafolio actual:
        saldo efectivo + suma (cantidad acciones * precio actual).
        """
        valor_acciones = 0.0
        for simbolo, cantidad in self._tenencias.items():
            precio_unitario = get_share_price(simbolo)
            valor_acciones += precio_unitario * cantidad
        return self._saldo_efectivo + valor_acciones

    def ganancias_perdidas(self) -> float:
        """
        Calcula y retorna la ganancia o pérdida neta en relación al depósito total:
        (valor_portafolio - deposito_inicial)
        Puede ser positivo o negativo.
        """
        return self.valor_portafolio() - self._deposito_inicial

    def listar_transacciones(self) -> List[Dict]:
        """
        Retorna la lista completa de transacciones realizadas en orden cronológico.
        Cada transacción incluye tipo, símbolo (si aplica), cantidad, precio unitario (si aplica), y fecha.
        """
        return list(self._transacciones)

    def _registrar_transaccion(
        self,
        tipo: str,
        simbolo: Optional[str] = None,
        cantidad: Optional[float] = None,
        precio_unitario: Optional[float] = None,
    ) -> None:
        """
        Registra una transacción con la información proporcionada y la fecha actual.
        """
        transaccion = {
            "tipo": tipo,
            "fecha": datetime.now().isoformat(),
        }
        if simbolo is not None:
            transaccion["simbolo"] = simbolo
        if cantidad is not None:
            transaccion["cantidad"] = cantidad
        if precio_unitario is not None:
            transaccion["precio_unitario"] = precio_unitario
        self._transacciones.append(transaccion)