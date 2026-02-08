import gradio as gr
from cuentas import Cuenta

def create_account(initial_deposit):
    try:
        account = Cuenta(float(initial_deposit))
        return "Cuenta creada con depósito inicial de ${:.2f}".format(initial_deposit), account
    except ValueError as e:
        return str(e), None

def deposit(account, amount):
    if not account:
        return "Por favor cree una cuenta primero", account
    try:
        account.deposit(float(amount))
        return "Depósito de ${:.2f} exitoso".format(amount), account
    except ValueError as e:
        return str(e), account

def withdraw(account, amount):
    if not account:
        return "Por favor cree una cuenta primero", account
    try:
        account.withdraw(float(amount))
        return "Retiro de ${:.2f} exitoso".format(amount), account
    except ValueError as e:
        return str(e), account

def buy_stock(account, symbol, quantity):
    if not account:
        return "Por favor cree una cuenta primero", account
    try:
        account.buy_stock(symbol, int(quantity))
        return "Compra de {} acciones de {} exitosa".format(quantity, symbol), account
    except ValueError as e:
        return str(e), account

def sell_stock(account, symbol, quantity):
    if not account:
        return "Por favor cree una cuenta primero", account
    try:
        account.sell_stock(symbol, int(quantity))
        return "Venta de {} acciones de {} exitosa".format(quantity, symbol), account
    except ValueError as e:
        return str(e), account

def get_portfolio_value(account):
    if not account:
        return "Por favor cree una cuenta primero"
    value = account.get_portfolio_value()
    return "Valor total del portafolio: ${:.2f}".format(value)

def get_profit_loss(account):
    if not account:
        return "Por favor cree una cuenta primero"
    profit = account.get_profit_loss()
    return "Ganancias/Pérdidas: ${:.2f}".format(profit)

def get_holdings(account):
    if not account:
        return "Por favor cree una cuenta primero"
    holdings = account.get_holdings()
    if not holdings:
        return "No posee ninguna acción"
    result = "Tenencias:\n"
    for symbol, data in holdings.items():
        result += "- {}: {} acciones (Costo base: ${:.2f})\n".format(symbol, data['quantity'], data['cost_basis'])
    return result

def get_transactions(account):
    if not account:
        return "Por favor cree una cuenta primero"
    transactions = account.get_transactions()
    if not transactions:
        return "No hay transacciones registradas"
    result = "Transacciones:\n"
    for tx in transactions:
        time_str = tx['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        if tx['type'] == 'deposit':
            result += "- {} {}: ${:.2f} (Saldo: ${:.2f})\n".format(tx['type'], tx['quantity'], tx['balance'], tx['balance'])
        elif tx['type'] == 'withdraw':
            result += "- {} {}: ${:.2f} (Saldo: ${:.2f})\n".format(tx['type'], tx['quantity'], tx['balance'], tx['balance'])
        else:
            result += "- {}: {} acciones de {} a ${:.2f} (Saldo: ${:.2f})\n".format(
                tx['type'],
                tx['quantity'],
                tx['symbol'],
                tx['price'],
                tx['balance']
            )
    return result

with gr.Blocks() as demo:
    account_state = gr.State(None)
    
    gr.Markdown("### Sistema de Gestión de Cuentas para Simulación de Trading")
    
    with gr.Row():
        initial_deposit = gr.Textbox(label="Depósito Inicial", placeholder="Ejemplo: 10000")
        create_btn = gr.Button("Crear Cuenta")
    
    with gr.Row():
        deposit_amount = gr.Textbox(label="Monto a Depositar", placeholder="Ejemplo: 500")
        deposit_btn = gr.Button("Depositar")
    
    with gr.Row():
        withdraw_amount = gr.Textbox(label="Monto a Retirar", placeholder="Ejemplo: 200")
        withdraw_btn = gr.Button("Retirar")
    
    with gr.Row():
        buy_symbol = gr.Textbox(label="Símbolo de Acción", placeholder="Ejemplo: AAPL")
        buy_quantity = gr.Textbox(label="Cantidad a Comprar", placeholder="Ejemplo: 10")
        buy_btn = gr.Button("Comprar")
    
    with gr.Row():
        sell_symbol = gr.Textbox(label="Símbolo de Acción", placeholder="Ejemplo: AAPL")
        sell_quantity = gr.Textbox(label="Cantidad a Vender", placeholder="Ejemplo: 5")
        sell_btn = gr.Button("Vender")
    
    with gr.Row():
        portfolio_output = gr.Textbox(label="Valor del Portafolio", interactive=False)
        profit_output = gr.Textbox(label="Ganancias/Pérdidas", interactive=False)
    
    with gr.Row():
        holdings_output = gr.Textbox(label="Tenencias", interactive=False)
        transactions_output = gr.Textbox(label="Transacciones", interactive=False)
    
    create_btn.click(fn=create_account, inputs=initial_deposit, outputs=[gr.Textbox(label="Estado"), account_state])
    deposit_btn.click(fn=deposit, inputs=[account_state, deposit_amount], outputs=[gr.Textbox(label="Estado"), account_state])
    withdraw_btn.click(fn=withdraw, inputs=[account_state, withdraw_amount], outputs=[gr.Textbox(label="Estado"), account_state])
    buy_btn.click(fn=buy_stock, inputs=[account_state, buy_symbol, buy_quantity], outputs=[gr.Textbox(label="Estado"), account_state])
    sell_btn.click(fn=sell_stock, inputs=[account_state, sell_symbol, sell_quantity], outputs=[gr.Textbox(label="Estado"), account_state])
    
    portfolio_output.change(fn=get_portfolio_value, inputs=account_state, outputs=portfolio_output)
    profit_output.change(fn=get_profit_loss, inputs=account_state, outputs=profit_output)
    holdings_output.change(fn=get_holdings, inputs=account_state, outputs=holdings_output)
    transactions_output.change(fn=get_transactions, inputs=account_state, outputs=transactions_output)

demo.launch()