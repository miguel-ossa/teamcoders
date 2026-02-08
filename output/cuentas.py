```python
def get_share_price(symbol: str) -> float:
    precios_prueba = {
        "AAPL": 190.0,
        "TSLA": 260.0,
        "GOOGL": 135.0
    }
    return precios_prueba.get(symbol, 0.0)

class Cuenta:
    def __init__(self, deposito_inicial: float):
        if deposito_inicial <= 0:
            raise ValueError("Depósito inicial debe ser positivo.")
        self.saldo = deposito_inicial
        self.portafolio = {}
        self.deposito_inicial = deposito_inicial
        self.transacciones = []

    def depositar(self, monto: float) -> None:
        if monto <= 0:
            raise ValueError("Monto debe ser positivo.")
        self.saldo += monto
        self.transacciones.append({
            'tipo': 'deposito',
            'monto': monto
        })

    def retirar(self, monto: float) -> None:
        if monto <= 0:
            raise ValueError("Monto debe ser positivo.")
        if self.saldo - monto < 0:
            raise ValueError("No se puede retirar fondos que dejen el saldo negativo.")
        self.saldo -= monto
        self.transacciones.append({
            'tipo': 'retiro',
            'monto': monto
        })

    def comprar(self, simbolo: str, cantidad: int) -> None:
        if not simbolo or not isinstance(simbolo, str):
            raise ValueError("Símbolo no puede estar vacío.")
        if cantidad <= 0:
            raise ValueError("Cantidad debe ser positiva.")
        precio = get_share_price(simbolo)
        total_costo = cantidad * precio
        if self.saldo < total_costo:
            raise ValueError("No tiene suficiente saldo para comprar.")
        self.saldo -= total_costo
        if simbolo in self.portafolio:
            self.portafolio[simbolo] += cantidad
        else:
            self.portafolio[simbolo] = cantidad
        self.transacciones.append({
            'tipo': 'compra',
            'simbolo': simbolo,
            'cantidad': cantidad,
            'monto': total_costo
        })

    def vender(self, simbolo: str, cantidad: int) -> None:
        if not simbolo or not isinstance(simbolo, str):
            raise ValueError("Símbolo no puede estar vacío.")
        if cantidad <= 0:
            raise ValueError("Cantidad debe ser positiva.")
        if simbolo not in self.portafolio or self.portafolio[simbolo] < cantidad:
            raise ValueError("No posee suficientes acciones para vender.")
        precio = get_share_price(simbolo)
        total_venta = cantidad * precio
        self.saldo += total_venta
        self.portafolio[simbolo] -= cantidad
        if self.portafolio[simbolo] == 0:
            del self.portafolio[simbolo]
        self.transacciones.append({
            'tipo': 'venta',
            'simbolo': simbolo,
            'cantidad': cantidad,
            'monto': total_venta
        })

    def valor_total_portafolio(self) -> float:
        total = 0.0
        for simbolo, cantidad in self.portafolio.items():
            total += cantidad * get_share_price(simbolo)
        return total

    def ganancias_o_perdidas(self) -> float:
        return self.valor_total_portafolio() - self.deposito_inicial

    def obtener_tenencias(self) -> dict:
        return self.portafolio.copy()

    def obtener_transacciones(self) -> list:
        return self.transacciones.copy()
```