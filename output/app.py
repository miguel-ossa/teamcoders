import gradio as gr
from cuentas import Cuenta, get_share_price

cuenta = None

def create_account(initial_balance: float) -> str:
    global cuenta
    if cuenta is not None:
        return "Cuenta ya existe. Use depositar o retirar."
    try:
        cuenta = Cuenta(initial_balance)
        return f"Cuenta creada con saldo inicial: {initial_balance}"
    except ValueError as e:
        return str(e)

def deposit(monto: float) -> str:
    global cuenta
    if cuenta is None:
        return "Cuenta no creada. Use crear cuenta primero."
    try:
        cuenta.depositar(monto)
        return f"Depósito de {monto} realizado. Saldo actual: {cuenta.saldo_actual}"
    except ValueError as e:
        return str(e)

def withdraw(monto: float) -> str:
    global cuenta
    if cuenta is None:
        return "Cuenta no creada. Use crear cuenta primero."
    try:
        cuenta.retirar(monto)
        return f"Retiro de {monto} realizado. Saldo actual: {cuenta.saldo_actual}"
    except ValueError as e:
        return str(e)

def buy_stock(symbol: str, quantity: int) -> str:
    global cuenta
    if cuenta is None:
        return "Cuenta no creada. Use crear cuenta primero."
    try:
        cuenta.comprar_acciones(symbol, quantity)
        return f"Compra de {quantity} acciones de {symbol} realizada. Saldo actual: {cuenta.saldo_actual}"
    except ValueError as e:
        return str(e)

def sell_stock(symbol: str, quantity: int) -> str:
    global cuenta
    if cuenta is None:
        return "Cuenta no creada. Use crear cuenta primero."
    try:
        cuenta.vender_acciones(symbol, quantity)
        return f"Venta de {quantity} acciones de {symbol} realizada. Saldo actual: {cuenta.saldo_actual}"
    except ValueError as e:
        return str(e)

def get_portfolio() -> str:
    global cuenta
    if cuenta is None:
        return "Cuenta no creada. Use crear cuenta primero."
    portafolio = cuenta.get_tenencias()
    if not portafolio:
        return "No hay tenencias."
    return "\n".join([f"{symbol}: {quantity} acciones" for symbol, quantity in portafolio.items()])

def get_gains() -> str:
    global cuenta
    if cuenta is None:
        return "Cuenta no creada. Use crear cuenta primero."
    gains = cuenta.calcular_ganancias_perdidas()
    return f"Ganancias o pérdidas: {gains:.2f}"

def list_transactions() -> str:
    global cuenta
    if cuenta is None:
        return "Cuenta no creada. Use crear cuenta primero."
    transactions = cuenta.listar_transacciones()
    if not transactions:
        return "No hay transacciones."
    return "\n".join([f"{t['tipo']}: {t['monto']} - Saldo: {t['saldo_actual']}" for t in transactions])

demo = gr.Blocks()

with demo:
    gr.Markdown("### Gestión de Cuentas de Trading")
    with gr.Tab("Crear Cuenta"):
        initial_balance = gr.Number(label="Saldo Inicial")
        create_btn = gr.Button("Crear Cuenta")
        create_output = gr.Textbox(label="Resultado")
        create_btn.click(fn=create_account, inputs=initial_balance, outputs=create_output)

    with gr.Tab("Depositar"):
        deposit_monto = gr.Number(label="Monto a Depositar")
        deposit_btn = gr.Button("Depositar")
        deposit_output = gr.Textbox(label="Resultado")
        deposit_btn.click(fn=deposit, inputs=deposit_monto, outputs=deposit_output)

    with gr.Tab("Retirar"):
        withdraw_monto = gr.Number(label="Monto a Retirar")
        withdraw_btn = gr.Button("Retirar")
        withdraw_output = gr.Textbox(label="Resultado")
        withdraw_btn.click(fn=withdraw, inputs=withdraw_monto, outputs=withdraw_output)

    with gr.Tab("Comprar Acciones"):
        symbol = gr.Textbox(label="Símbolo de Acción (ej: AAPL)")
        quantity = gr.Number(label="Cantidad")
        buy_btn = gr.Button("Comprar")
        buy_output = gr.Textbox(label="Resultado")
        buy_btn.click(fn=buy_stock, inputs=[symbol, quantity], outputs=buy_output)

    with gr.Tab("Vender Acciones"):
        symbol = gr.Textbox(label="Símbolo de Acción (ej: AAPL)")
        quantity = gr.Number(label="Cantidad")
        sell_btn = gr.Button("Vender")
        sell_output = gr.Textbox(label="Resultado")
        sell_btn.click(fn=sell_stock, inputs=[symbol, quantity], outputs=sell_output)

    with gr.Tab("Ver Tenencias"):
        portfolio_btn = gr.Button("Ver Tenencias")
        portfolio_output = gr.Textbox(label="Tenencias")
        portfolio_btn.click(fn=get_portfolio, inputs=[], outputs=portfolio_output)

    with gr.Tab("Ver Ganancias/Pérdidas"):
        gains_btn = gr.Button("Ver Ganancias")
        gains_output = gr.Textbox(label="Ganancias/Pérdidas")
        gains_btn.click(fn=get_gains, inputs=[], outputs=gains_output)

    with gr.Tab("Lista de Transacciones"):
        transactions_btn = gr.Button("Ver Transacciones")
        transactions_output = gr.Textbox(label="Transacciones")
        transactions_btn.click(fn=list_transactions, inputs=[], outputs=transactions_output)

demo.launch()