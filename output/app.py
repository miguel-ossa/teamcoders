import gradio as gr
from cuentas import Cuenta

# Inicializar una cuenta para demostración
cuenta = Cuenta(user_id="user1", initial_deposit=1000.0)

def create_account(initial_deposit):
    global cuenta
    cuenta = Cuenta(user_id="user1", initial_deposit=initial_deposit)
    return f"Cuenta creada con un depósito inicial de: {initial_deposit}"

def deposit(amount):
    success = cuenta.deposit(amount)
    if success:
        return f"Depósito exitoso. Balance actual: {cuenta.balance}"
    else:
        return "Depósito fallido. Asegúrese de que el monto sea positivo."

def withdraw(amount):
    success = cuenta.withdraw(amount)
    if success:
        return f"Retiro exitoso. Balance actual: {cuenta.balance}"
    else:
        return "Retiro fallido. Verifique que tenga fondos suficientes y que el monto sea positivo."

def buy_shares(symbol, quantity):
    success = cuenta.buy_shares(symbol, int(quantity))
    if success:
        return f"Compra exitosa de {quantity} acciones de {symbol}. Balance actual: {cuenta.balance}"
    else:
        return "Compra fallida. Verifique su balance y la cantidad solicitada."

def sell_shares(symbol, quantity):
    success = cuenta.sell_shares(symbol, int(quantity))
    if success:
        return f"Venta exitosa de {quantity} acciones de {symbol}. Balance actual: {cuenta.balance}"
    else:
        return "Venta fallida. Verifique si posee suficientes acciones."

def calculate_portfolio_value():
    total_value = cuenta.calculate_portfolio_value()
    return f"Valor total del portafolio: {total_value}"

def get_gains_or_losses():
    gains_or_losses = cuenta.get_gains_or_losses()
    return f"Ganancias/Pérdidas actuales: {gains_or_losses}"

def get_holdings():
    holdings = cuenta.get_holdings()
    return f"Tenencias actuales: {holdings}"

def list_transactions():
    transactions = cuenta.list_transactions()
    return f"Transacciones: {transactions}"

interface = gr.Interface(
    fn=[
        create_account,
        deposit,
        withdraw,
        buy_shares,
        sell_shares,
        calculate_portfolio_value,
        get_gains_or_losses,
        get_holdings,
        list_transactions
    ],
    inputs=[
        gr.inputs.Number(label="Depósito inicial"),
        gr.inputs.Number(label="Monto a depositar"),
        gr.inputs.Number(label="Monto a retirar"),
        gr.inputs.Textbox(label="Símbolo para comprar"),
        gr.inputs.Number(label="Cantidad para comprar"),
        gr.inputs.Textbox(label="Símbolo para vender"),
        gr.inputs.Number(label="Cantidad para vender"),
        gr.inputs.Textbox(visible=False),  # No se requiere para cálculo de valor
        gr.inputs.Textbox(visible=False),  # No se requiere para ganancias/pérdidas
        gr.inputs.Textbox(visible=False),  # No se requiere para tenencias
        gr.inputs.Textbox(visible=False)   # No se requiere para transacciones
    ],
    outputs=[
        gr.outputs.Textbox(label="Resultado de creación de cuenta"),
        gr.outputs.Textbox(label="Resultado de depósito"),
        gr.outputs.Textbox(label="Resultado de retiro"),
        gr.outputs.Textbox(label="Resultado de compra"),
        gr.outputs.Textbox(label="Resultado de venta"),
        gr.outputs.Textbox(label="Valor del portafolio"),
        gr.outputs.Textbox(label="Ganancias/Pérdidas"),
        gr.outputs.Textbox(label="Tenencias"),
        gr.outputs.Textbox(label="Transacciones")
    ],
    live=False
)

interface.launch()