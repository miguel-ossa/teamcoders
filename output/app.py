import gradio as gr
from cuentas import Cuenta, get_share_price

cuenta = Cuenta(10000)

def get_balance():
    return f"Saldo: ${cuenta.saldo:.2f}"

def get_portfolio():
    if not cuenta.portafolio:
        return "No hay tenencias."
    return "\n".join([f"{symbol}: {cantidad} acciones" for symbol, cantidad in cuenta.portafolio.items()])

def get_gains():
    gains = cuenta.ganancias_o_perdidas()
    return f"Ganancias/Pérdidas: ${gains:.2f}"

def get_transactions():
    if not cuenta.transacciones:
        return "No hay transacciones."
    return "\n".join([f"{t['tipo']}: {t.get('monto', '')}" for t in cuenta.transacciones])

def depositar(monto):
    try:
        cuenta.depositar(monto)
        return get_balance(), get_portfolio(), get_gains(), get_transactions()
    except Exception as e:
        return str(e), get_portfolio(), get_gains(), get_transactions()

def retirar(monto):
    try:
        cuenta.retirar(monto)
        return get_balance(), get_portfolio(), get_gains(), get_transactions()
    except Exception as e:
        return str(e), get_portfolio(), get_gains(), get_transactions()

def comprar(simbolo, cantidad):
    try:
        cuenta.comprar(simbolo, cantidad)
        return get_balance(), get_portfolio(), get_gains(), get_transactions()
    except Exception as e:
        return str(e), get_portfolio(), get_gains(), get_transactions()

def vender(simbolo, cantidad):
    try:
        cuenta.vender(simbolo, cantidad)
        return get_balance(), get_portfolio(), get_gains(), get_transactions()
    except Exception as e:
        return str(e), get_portfolio(), get_gains(), get_transactions()

def create_account(deposito_inicial):
    global cuenta
    try:
        cuenta = Cuenta(deposito_inicial)
        return get_balance(), get_portfolio(), get_gains(), get_transactions()
    except Exception as e:
        return str(e), get_portfolio(), get_gains(), get_transactions()

with gr.Blocks() as demo:
    gr.Markdown("## Gestión de Cuenta de Trading")
    
    with gr.Row():
        deposito_input = gr.Number(label="Depósito Inicial", value=10000)
        create_button = gr.Button("Crear Cuenta")
    
    with gr.Row():
        deposito_amount = gr.Number(label="Monto a Depositar")
        deposit_button = gr.Button("Depositar")
    
    with gr.Row():
        withdraw_amount = gr.Number(label="Monto a Retirar")
        withdraw_button = gr.Button("Retirar")
    
    with gr.Row():
        buy_symbol = gr.Text(label="Símbolo (AAPL, TSLA, GOOGL)")
        buy_quantity = gr.Number(label="Cantidad a Comprar")
        buy_button = gr.Button("Comprar")
    
    with gr.Row():
        sell_symbol = gr.Text(label="Símbolo (AAPL, TSLA, GOOGL)")
        sell_quantity = gr.Number(label="Cantidad a Vender")
        sell_button = gr.Button("Vender")
    
    with gr.Row():
        balance_output = gr.Textbox(label="Saldo Actual", interactive=False)
        portfolio_output = gr.Textbox(label="Tenencias", interactive=False)
        gains_output = gr.Textbox(label="Ganancias/Pérdidas", interactive=False)
        transactions_output = gr.Textbox(label="Transacciones", interactive=False)
    
    create_button.click(fn=create_account, inputs=deposito_input, outputs=[balance_output, portfolio_output, gains_output, transactions_output])
    deposit_button.click(fn=depositar, inputs=deposito_amount, outputs=[balance_output, portfolio_output, gains_output, transactions_output])
    withdraw_button.click(fn=retirar, inputs=withdraw_amount, outputs=[balance_output, portfolio_output, gains_output, transactions_output])
    buy_button.click(fn=comprar, inputs=[buy_symbol, buy_quantity], outputs=[balance_output, portfolio_output, gains_output, transactions_output])
    sell_button.click(fn=vender, inputs=[sell_symbol, sell_quantity], outputs=[balance_output, portfolio_output, gains_output, transactions_output])

demo.launch()