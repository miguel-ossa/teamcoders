import datetime

def get_share_price(symbol: str) -> float:
    precios_prueba = {
        "AAPL": 190.0,
        "TSLA": 260.0,
        "GOOGL": 135.0
    }
    return precios_prueba.get(symbol, 0.0)

class Cuenta:
    def __init__(self, usuario: str, deposito_inicial: float):
        if deposito_inicial <= 0:
            raise ValueError("Depósito inicial debe ser positivo")
        self.usuario = usuario
        self.saldo = deposito_inicial
        self.tenencias = {}
        self.transacciones = []
        self.deposito_inicial = deposito_inicial

    def depositar(self, monto: float) -> None:
        if monto <= 0:
            raise ValueError("Monto debe ser positivo")
        self.saldo += monto
        self._registrar_transaccion("depósito", "", 0, 0.0)

    def retirar(self, monto: float) -> None:
        if monto <= 0:
            raise ValueError("Monto debe ser positivo")
        if self.saldo - monto < 0:
            raise ValueError("No se puede retirar fondos que dejan el saldo negativo")
        self.saldo -= monto
        self._registrar_transaccion("retiro", "", 0, 0.0)

    def comprar_acciones(self, simbolo: str, cantidad: int) -> None:
        if cantidad <= 0:
            raise ValueError("Cantidad debe ser positiva")
        precio = get_share_price(simbolo)
        if precio == 0:
            raise ValueError("Símbolo no válido")
        costo_total = cantidad * precio
        if self.saldo < costo_total:
            raise ValueError("Saldo insuficiente para comprar")
        self.saldo -= costo_total
        if simbolo in self.tenencias:
            self.tenencias[simbolo] += cantidad
        else:
            self.tenencias[simbolo] = cantidad
        self._registrar_transaccion("compra", simbolo, cantidad, precio)

    def vender_acciones(self, simbolo: str, cantidad: int) -> None:
        if cantidad <= 0:
            raise ValueError("Cantidad debe ser positiva")
        if simbolo not in self.tenencias or self.tenencias[simbolo] < cantidad:
            raise ValueError("No se poseen suficientes acciones para vender")
        precio = get_share_price(simbolo)
        if precio == 0:
            raise ValueError("Símbolo no válido")
        valor_venta = cantidad * precio
        self.saldo += valor_venta
        self.tenencias[simbolo] -= cantidad
        self._registrar_transaccion("venta", simbolo, cantidad, precio)

    def calcular_valor_total(self) -> float:
        valor_total = self.saldo
        for simbolo, cantidad in self.tenencias.items():
            precio = get_share_price(simbolo)
            valor_total += cantidad * precio
        return valor_total

    def calcular_ganancias_perdidas(self) -> float:
        return self.calcular_valor_total() - self.deposito_inicial

    def obtener_tenencias(self) -> dict:
        return self.tenencias

    def listar_transacciones(self) -> list:
        return self.transacciones

    def _registrar_transaccion(self, tipo: str, simbolo: str, cantidad: int, precio: float) -> None:
        transaccion = {
            "tipo": tipo,
            "simbolo": simbolo,
            "cantidad": cantidad,
            "precio": precio,
            "timestamp": datetime.datetime.now().isoformat()
        }
        self.transacciones.append(transaccion)