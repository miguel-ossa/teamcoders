import unittest
from cuentas import Cuenta

class TestCuenta(unittest.TestCase):
    def test_initial_deposit_positive(self):
        cuenta = Cuenta(1000)
        self.assertEqual(cuenta.balance, 1000)
        self.assertEqual(cuenta.initial_deposit, 1000)
    
    def test_initial_deposit_zero(self):
        with self.assertRaises(ValueError):
            Cuenta(0)
    
    def test_initial_deposit_negative(self):
        with self.assertRaises(ValueError):
            Cuenta(-100)
    
    def test_deposit_positive(self):
        cuenta = Cuenta(1000)
        cuenta.deposit(500)
        self.assertEqual(cuenta.balance, 1500)
    
    def test_deposit_zero(self):
        cuenta = Cuenta(1000)
        with self.assertRaises(ValueError):
            cuenta.deposit(0)
    
    def test_deposit_negative(self):
        cuenta = Cuenta(1000)
        with self.assertRaises(ValueError):
            cuenta.deposit(-500)
    
    def test_withdraw_positive(self):
        cuenta = Cuenta(1000)
        cuenta.withdraw(500)
        self.assertEqual(cuenta.balance, 500)
    
    def test_withdraw_insufficient(self):
        cuenta = Cuenta(1000)
        with self.assertRaises(ValueError):
            cuenta.withdraw(1500)
    
    def test_withdraw_zero(self):
        cuenta = Cuenta(1000)
        with self.assertRaises(ValueError):
            cuenta.withdraw(0)
    
    def test_withdraw_negative(self):
        cuenta = Cuenta(1000)
        with self.assertRaises(ValueError):
            cuenta.withdraw(-500)
    
    def test_buy_stock_valid(self):
        cuenta = Cuenta(1000)
        cuenta.buy_stock('AAPL', 2)
        self.assertEqual(cuenta.balance, 700)
        self.assertEqual(cuenta.holdings['AAPL']['quantity'], 2)
        self.assertEqual(cuenta.holdings['AAPL']['cost_basis'], 300)
    
    def test_buy_stock_insufficient_funds(self):
        cuenta = Cuenta(100)
        with self.assertRaises(ValueError):
            cuenta.buy_stock('AAPL', 2)
    
    def test_buy_stock_invalid_symbol(self):
        cuenta = Cuenta(1000)
        with self.assertRaises(ValueError):
            cuenta.buy_stock('XYZ', 1)
    
    def test_sell_stock_valid(self):
        cuenta = Cuenta(1000)
        cuenta.buy_stock('AAPL', 2)
        cuenta.sell_stock('AAPL', 1)
        self.assertEqual(cuenta.balance, 850)
        self.assertEqual(cuenta.holdings['AAPL']['quantity'], 1)
        self.assertEqual(cuenta.holdings['AAPL']['cost_basis'], 300)
    
    def test_sell_stock_insufficient(self):
        cuenta = Cuenta(1000)
        with self.assertRaises(ValueError):
            cuenta.sell_stock('AAPL', 1)
    
    def test_sell_stock_invalid_quantity(self):
        cuenta = Cuenta(1000)
        with self.assertRaises(ValueError):
            cuenta.sell_stock('AAPL', 0)
    
    def test_get_portfolio_value(self):
        cuenta = Cuenta(1000)
        cuenta.buy_stock('AAPL', 2)
        self.assertEqual(cuenta.get_portfolio_value(), 1000)
    
    def test_get_profit_loss(self):
        cuenta = Cuenta(1000)
        cuenta.buy_stock('AAPL', 2)
        self.assertEqual(cuenta.get_profit_loss(), 0)
    
    def test_get_holdings(self):
        cuenta = Cuenta(1000)
        cuenta.buy_stock('AAPL', 2)
        self.assertEqual(cuenta.get_holdings(), {'AAPL': {'quantity': 2, 'cost_basis': 300}})
    
    def test_get_transactions(self):
        cuenta = Cuenta(1000)
        cuenta.deposit(500)
        cuenta.withdraw(200)
        cuenta.buy_stock('AAPL', 1)
        transactions = cuenta.get_transactions()
        self.assertEqual(len(transactions), 3)
        self.assertEqual(transactions[0]['type'], 'deposit')
        self.assertEqual(transactions[1]['type'], 'withdraw')
        self.assertEqual(transactions[2]['type'], 'buy')

if __name__ == '__main__':
    unittest.main()