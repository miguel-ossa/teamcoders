# Definición de la clase Cuenta en el módulo cuentas.py

class Cuenta:
    def __init__(self, user_id: str, initial_deposit: float) -> None:
        self.user_id = user_id
        self.initial_deposit = initial_deposit
        self.balance = initial_deposit
        self.portfolio = {}
        self.transactions = []

    def deposit(self, amount: float) -> bool:
        if amount <= 0:
            return False
        self.balance += amount
        self.transactions.append({
            'type': 'deposit',
            'amount': amount
        })
        return True

    def withdraw(self, amount: float) -> bool:
        if amount > self.balance or amount <= 0:
            return False
        self.balance -= amount
        self.transactions.append({
            'type': 'withdraw',
            'amount': amount
        })
        return True

    def buy_shares(self, symbol: str, quantity: int) -> bool:
        price = get_share_price(symbol)
        cost = price * quantity
        if cost > self.balance or quantity <= 0:
            return False
        self.balance -= cost
        if symbol in self.portfolio:
            self.portfolio[symbol] += quantity
        else:
            self.portfolio[symbol] = quantity
        self.transactions.append({
            'type': 'buy',
            'symbol': symbol,
            'quantity': quantity,
            'price': price
        })
        return True

    def sell_shares(self, symbol: str, quantity: int) -> bool:
        if symbol not in self.portfolio or self.portfolio[symbol] < quantity or quantity <= 0:
            return False
        price = get_share_price(symbol)
        self.balance += price * quantity
        self.portfolio[symbol] -= quantity
        if self.portfolio[symbol] == 0:
            del self.portfolio[symbol]
        self.transactions.append({
            'type': 'sell',
            'symbol': symbol,
            'quantity': quantity,
            'price': price
        })
        return True

    def calculate_portfolio_value(self) -> float:
        total_value = 0.0
        for symbol, quantity in self.portfolio.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def get_gains_or_losses(self) -> float:
        current_portfolio_value = self.calculate_portfolio_value()
        current_balance = self.balance
        total_value = current_balance + current_portfolio_value
        return total_value - self.initial_deposit

    def get_holdings(self) -> dict:
        return self.portfolio.copy()

    def list_transactions(self) -> list:
        return self.transactions.copy()

def get_share_price(symbol: str) -> float:
    prices = {
        'AAPL': 150.0,
        'TSLA': 700.0,
        'GOOGL': 2800.0
    }
    return prices.get(symbol, 0.0)