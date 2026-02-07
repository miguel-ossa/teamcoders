class Cuenta:
    def __init__(self, user_id: str, initial_deposit: float) -> None:
        self.user_id = user_id
        self.initial_deposit = initial_deposit
        self.balance = initial_deposit
        self.portfolio = {}
        self.transactions = []

    def depositar_fondos(self, monto: float) -> None:
        self.balance += monto
        self.transactions.append(('depósito', None, monto, None))

    def retirar_fondos(self, monto: float) -> bool:
        if monto > self.balance:
            return False
        self.balance -= monto
        self.transactions.append(('retiro', None, monto, None))
        return True

    def comprar_acciones(self, simbolo: str, cantidad: int) -> bool:
        precio = get_share_pryce(simbolo)
        costo_total = precio * cantidad

        if costo_total > self.balance:
            return False
        
        self.balance -= costo_total
        if simbolo in self.portfolio:
            self.portfolio[simbolo] += cantidad
        else:
            self.portfolio[simbolo] = cantidad
        self.transactions.append(('compra', simbolo, cantidad, precio))
        return True

    def vender_acciones(self, simbolo: str, cantidad: int) -> bool:
        if simbolo not in self.portfolio or self.portfolio[simbolo] < cantidad:
            return False

        precio = get_share_pryce(simbolo)
        ingreso_total = precio * cantidad

        self.balance += ingreso_total
        self.portfolio[simbolo] -= cantidad
        if self.portfolio[simbolo] == 0:
            del self.portfolio[simbolo]

        self.transactions.append(('venta', simbolo, cantidad, precio))
        return True

    def valor_portafolio(self) -> float:
        valor_total = 0
        for simbolo, cantidad in self.portfolio.items():
            valor_total += get_share_pryce(simbolo) * cantidad
        return valor_total

    def ganancias_perdidas(self) -> float:
        return (self.valor_portafolio() + self.balance) - self.initial_deposit

    def informar_tenencias(self) -> dict:
        return self.portfolio.copy()

    def informar_transacciones(self) -> list:
        return self.transactions.copy()

def get_share_pryce(symbol: str) -> float:
    precios = {
        'AAPL': 150.0,
        'TSLA': 650.0,
        'GOOGL': 2800.0
    }
    return precios.get(symbol.upper(), 0.0)