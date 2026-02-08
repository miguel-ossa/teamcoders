import datetime

def get_share_price(symbol):
    if symbol == 'AAPL':
        return 150.0
    elif symbol == 'TSLA':
        return 250.0
    elif symbol == 'GOOGL':
        return 130.0
    else:
        raise ValueError("Symbol not found")

class Cuenta:
    def __init__(self, initial_deposit: float):
        if initial_deposit <= 0:
            raise ValueError("Initial deposit must be positive")
        self.balance = initial_deposit
        self.initial_deposit = initial_deposit
        self.holdings = {}
        self.transactions = []

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        self._record_transaction("deposit", amount=amount)

    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Withdraw amount must be positive")
        if self.balance - amount < 0:
            raise ValueError("Cannot withdraw, insufficient balance")
        self.balance -= amount
        self._record_transaction("withdraw", amount=amount)

    def buy_stock(self, symbol: str, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        price = get_share_price(symbol)
        total_cost = price * quantity
        if self.balance < total_cost:
            raise ValueError("Insufficient funds to buy")
        self.balance -= total_cost
        if symbol in self.holdings:
            self.holdings[symbol]['quantity'] += quantity
            self.holdings[symbol]['cost_basis'] += total_cost
        else:
            self.holdings[symbol] = {
                'quantity': quantity,
                'cost_basis': total_cost
            }
        self._record_transaction("buy", symbol=symbol, quantity=quantity, price=price)

    def sell_stock(self, symbol: str, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if symbol not in self.holdings or self.holdings[symbol]['quantity'] < quantity:
            raise ValueError("Not enough shares to sell")
        price = get_share_price(symbol)
        proceeds = price * quantity
        self.balance += proceeds
        self.holdings[symbol]['quantity'] -= quantity
        if self.holdings[symbol]['quantity'] == 0:
            del self.holdings[symbol]
        self._record_transaction("sell", symbol=symbol, quantity=quantity, price=price)

    def get_portfolio_value(self) -> float:
        portfolio_value = self.balance
        for symbol, data in self.holdings.items():
            price = get_share_price(symbol)
            portfolio_value += data['quantity'] * price
        return portfolio_value

    def get_profit_loss(self) -> float:
        return self.get_portfolio_value() - self.initial_deposit

    def get_holdings(self) -> dict:
        return self.holdings

    def get_transactions(self) -> list:
        return self.transactions

    def _record_transaction(self, transaction_type: str, **kwargs):
        timestamp = datetime.datetime.now()
        transaction = {
            'type': transaction_type,
            'timestamp': timestamp,
            'balance': self.balance
        }
        if transaction_type == 'deposit':
            transaction['quantity'] = kwargs['amount']
        elif transaction_type == 'withdraw':
            transaction['quantity'] = kwargs['amount']
        elif transaction_type in ['buy', 'sell']:
            transaction['symbol'] = kwargs['symbol']
            transaction['quantity'] = kwargs['quantity']
            transaction['price'] = kwargs['price']
        self.transactions.append(transaction)