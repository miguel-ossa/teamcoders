```python
def get_share_price(symbol: str) -> float:
    test_prices = {
        'AAPL': 150.0,
        'TSLA': 250.0,
        'GOOGL': 130.0
    }
    return test_prices.get(symbol, 0.0)

class Cuenta:
    def __init__(self, saldo_inicial: float):
        if not isinstance(saldo_inicial, (int, float)) or saldo_inicial <= 0:
            raise ValueError("Saldo inicial debe ser un número positivo")
        self.saldo_inicial = float(saldo_inicial)
        self.saldo_actual = float(saldo_inicial)
        self.portafolio = {}
        self.transacciones = []

    def depositar(self, monto: float) -> None:
        if not isinstance(monto, (int, float)) or monto <= 0:
            raise ValueError("Monto debe ser un número positivo")
        self.saldo_actual += monto
        self.transacciones.append({
            'tipo': 'depósito',
            'monto': monto,
            'saldo_actual': self.saldo_actual
        })

    def retirar(self, monto: float) -> None:
        if not isinstance(monto, (int, float)) or monto <= 0:
            raise ValueError("Monto debe ser un número positivo")
        if self.saldo_actual - monto < 0:
            raise ValueError("No se puede retirar fondos que dejen el saldo negativo")
        self.saldo_actual -= monto
        self.transacciones.append({
            'tipo': 'retiro',
            'monto': monto,
            'saldo_actual': self.saldo_actual
        })

    def comprar_acciones(self, simbolo: str, cantidad: int) -> None:
        if not isinstance(simbolo, str) or len(simbolo) == 0:
            raise ValueError("Símbolo de acción no puede estar vacío")
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("Cantidad debe ser un entero positivo")
        precio = get_share_price(simbolo)
        costo_total = precio * cantidad
        if self.saldo_actual < costo_total:
            raise ValueError("Fondos insuficientes para comprar las acciones")
        self.saldo_actual -= costo_total
        if simbolo in self.portafolio:
            self.portafolio[simbolo] += cantidad
        else:
            self.portafolio[simbolo] = cantidad
        self.transacciones.append({
            'tipo': 'compra',
            'simbolo': simbolo,
            'cantidad': cantidad,
            'precio': precio,
            'saldo_actual': self.saldo_actual
        })

    def vender_acciones(self, simbolo: str, cantidad: int) -> None:
        if not isinstance(simbolo, str) or len(simbolo) == 0:
            raise ValueError("Símbolo de acción no puede estar vacío")
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("Cantidad debe ser un entero positivo")
        if simbolo not in self.portafolio or self.portafolio[simbolo] < cantidad:
            raise ValueError("No se poseen suficientes acciones para vender")
        precio = get_share_price(simbolo)
        ganancia = precio * cantidad
        self.saldo_actual += ganancia
        self.portafolio[simbolo] -= cantidad
        if self.portafolio[simbolo] == 0:
            del self.portafolio[simbolo]
        self.transacciones.append({
            'tipo': 'venta',
            'simbolo': simbolo,
            'cantidad': cantidad,
            'precio': precio,
            'saldo_actual': self.saldo_actual
        })

    def calcular_valor_total(self) -> float:
        valor_total = 0.0
        for simbolo, cantidad in self.portafolio.items():
            precio = get_share_price(simbolo)
            valor_total += precio * cantidad
        return valor_total

    def calcular_ganancias_perdidas(self) -> float:
        valor_total = self.calcular_valor_total()
        return valor_total - self.saldo_inicial

    def get_tenencias(self) -> dict[str, int]:
        return self.portafolio.copy()

    def listar_transacciones(self) -> list[dict]:
        return self.transacciones.copy()
```