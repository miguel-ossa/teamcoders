import gradio as gr
from cuentas import Cuenta

def create_account(username, deposit, state):
    if state is not None:
        return state, "Account already exists"
    try:
        account = Cuenta(username, deposit)
        return account, "Account created"
    except ValueError as e:
        return state, str(e)

def deposit(monto, state):
    if state is None:
        return state, "Please create an account first"
    try:
        state.depositar(monto)
        return state, f"Deposited {monto}. New balance: {state.saldo}"
    except ValueError as e:
        return state, str(e)

def withdraw(monto, state):
    if state is None:
        return state, "Please create an account first"
    try:
        state.retirar(monto)
        return state, f"Withdrew {monto}. New balance: {state.saldo}"
    except ValueError as e:
        return state, str(e)

def buy_stock(symbol, quantity, state):
    if state is None:
        return state, "Please create an account first"
    try:
        state.comprar_acciones(symbol, quantity)
        return state, f"Bought {quantity} of {symbol}. New balance: {state.saldo}"
    except ValueError as e:
        return state, str(e)

def sell_stock(symbol, quantity, state):
    if state is None:
        return state, "Please create an account first"
    try:
        state.vender_acciones(symbol, quantity)
        return state, f"Sold {quantity} of {symbol}. New balance: {state.saldo}"
    except ValueError as e:
        return state, str(e)

def get_balance(state):
    if state is None:
        return "No account created"
    return f"Current Balance: {state.saldo}"

def get_holdings(state):
    if state is None:
        return "No account created"
    return f"Holdings: {state.obtener_tenencias()}"

def get_portfolio_value(state):
    if state is None:
        return "No account created"
    return f"Portfolio Value: {state.calcular_valor_total()}"

def get_gains_losses(state):
    if state is None:
        return "No account created"
    return f"Gains/Losses: {state.calcular_ganancias_perdidas()}"

def get_transactions(state):
    if state is None:
        return "No account created"
    return "Transactions:\n" + "\n".join([f"{t['tipo']} {t['simbolo']} {t['cantidad']} @ {t['precio']} ({t['timestamp']})" for t in state.listar_transacciones()])

with gr.Blocks() as demo:
    state = gr.State()
    
    gr.Markdown("## Trading Account Management Demo")
    
    with gr.Row():
        with gr.Column():
            username_input = gr.Textbox(label="Username")
            deposit_input = gr.Number(label="Initial Deposit", minimum=0)
            create_button = gr.Button("Create Account")
            create_output = gr.Textbox(label="Status")
            
            create_button.click(fn=create_account, inputs=[username_input, deposit_input, state], outputs=[state, create_output])
            
            deposit_input2 = gr.Number(label="Deposit Amount", minimum=0)
            deposit_button = gr.Button("Deposit")
            deposit_output = gr.Textbox(label="Deposit Result")
            
            deposit_button.click(fn=deposit, inputs=[deposit_input2, state], outputs=[state, deposit_output])
            
            withdraw_input = gr.Number(label="Withdraw Amount", minimum=0)
            withdraw_button = gr.Button("Withdraw")
            withdraw_output = gr.Textbox(label="Withdraw Result")
            
            withdraw_button.click(fn=withdraw, inputs=[withdraw_input, state], outputs=[state, withdraw_output])
            
            buy_symbol = gr.Textbox(label="Stock Symbol (e.g., AAPL)")
            buy_quantity = gr.Number(label="Quantity", minimum=0)
            buy_button = gr.Button("Buy Stock")
            buy_output = gr.Textbox(label="Buy Result")
            
            buy_button.click(fn=buy_stock, inputs=[buy_symbol, buy_quantity, state], outputs=[state, buy_output])
            
            sell_symbol = gr.Textbox(label="Stock Symbol (e.g., TSLA)")
            sell_quantity = gr.Number(label="Quantity", minimum=0)
            sell_button = gr.Button("Sell Stock")
            sell_output = gr.Textbox(label="Sell Result")
            
            sell_button.click(fn=sell_stock, inputs=[sell_symbol, sell_quantity, state], outputs=[state, sell_output])
            
        with gr.Column():
            balance_output = gr.Textbox(label="Current Balance", value=get_balance(state))
            holdings_output = gr.Textbox(label="Holdings", value=get_holdings(state))
            portfolio_output = gr.Textbox(label="Portfolio Value", value=get_portfolio_value(state))
            gains_output = gr.Textbox(label="Gains/Losses", value=get_gains_losses(state))
            transactions_output = gr.Textbox(label="Transactions", value=get_transactions(state))
    
demo.launch()