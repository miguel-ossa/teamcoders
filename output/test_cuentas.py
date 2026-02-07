from cuentas import Cuenta, get_share_price
import unittest

class TestCuenta(unittest.TestCase):

    def setUp(self):
        self.cuenta = Cuenta(user_id='test_user', initial_deposit=1000.0)

    def test_deposit_positive_amount(self):
        result = self.cuenta.deposit(500.0)
        self.assertTrue(result)
        self.assertEqual(self.cuenta.balance, 1500.0)

    def test_deposit_negative_amount(self):
        result = self.cuenta.deposit(-500.0)
        self.assertFalse(result)
        self.assertEqual(self.cuenta.balance, 1000.0)

    def test_withdraw_valid_amount(self):
        result = self.cuenta.withdraw(500.0)
        self.assertTrue(result)
        self.assertEqual(self.cuenta.balance, 500.0)

    def test_withdraw_invalid_amount(self):
        result = self.cuenta.withdraw(1500.0)
        self.assertFalse(result)
        self.assertEqual(self.cuenta.balance, 1000.0)

    def test_buy_shares_valid(self):
        result = self.cuenta.buy_shares('AAPL', 5)
        self.assertTrue(result)
        self.assertEqual(self.cuenta.balance, 250.0)
        self.assertEqual(self.cuenta.portfolio['AAPL'], 5)

    def test_buy_shares_insufficient_funds(self):
        result = self.cuenta.buy_shares('GOOGL', 1)
        self.assertFalse(result)
        self.assertEqual(self.cuenta.balance, 1000.0)

    def test_sell_shares_valid(self):
        self.cuenta.buy_shares('AAPL', 5)
        result = self.cuenta.sell_shares('AAPL', 3)
        self.assertTrue(result)
        self.assertEqual(self.cuenta.balance, 700.0)
        self.assertEqual(self.cuenta.portfolio['AAPL'], 2)

    def test_sell_shares_invalid(self):
        result = self.cuenta.sell_shares('AAPL', 3)
        self.assertFalse(result)
        self.assertEqual(self.cuenta.balance, 1000.0)

    def test_calculate_portfolio_value(self):
        self.cuenta.buy_shares('AAPL', 5)
        self.assertEqual(self.cuenta.calculate_portfolio_value(), 750.0)

    def test_get_gains_or_losses(self):
        self.cuenta.buy_shares('AAPL', 5)
        self.assertEqual(self.cuenta.get_gains_or_losses(), 0.0)

    def test_get_holdings(self):
        self.cuenta.buy_shares('AAPL', 5)
        holdings = self.cuenta.get_holdings()
        self.assertEqual(holdings['AAPL'], 5)

    def test_list_transactions(self):
        self.cuenta.deposit(500.0)
        transactions = self.cuenta.list_transactions()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]['type'], 'deposit')

if __name__ == '__main__':
    unittest.main()