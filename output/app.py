import os
import json
from flask import Flask, request, jsonify, render_template_string
from cuentas import Cuenta, get_share_pryce

app = Flask(__name__)

# Crear una única instancia de cuenta para el usuario
cuenta = Cuenta()

# Plantilla HTML para la interfaz
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simulador de Trading</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
        }
        .container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        .panel {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .panel h2 {
            color: #34495e;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            margin-top: 0;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input[type="number"], input[type="text"] {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }
        button:hover {
            background-color: #2980b9;
        }
        button.sell {
            background-color: #e74c3c;
        }
        button.sell:hover {
            background-color: #c0392b;
        }
        button.deposit {
            background-color: #27ae60;
        }
        button.deposit:hover {
            background-color: #219a52;
        }
        button.withdraw {
            background-color: #e67e22;
        }
        button.withdraw:hover {
            background-color: #d35400;
        }
        .stats {
            background: #ecf0f1;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .stat-item {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
        }
        .stat-value {
            font-weight: bold;
            color: #2c3e50;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f8f9fa;
            font-weight: bold;
        }
        .success {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 15px;
        }
        .error {
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 15px;
        }
        .actions {
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }
        .action-btn {
            flex: 1;
            padding: 8px;
            text-align: center;
        }
    </style>
</head>
<body>
    <h1>Simulador de Trading</h1>
    
    {% if message %}
    <div class="{{ message_type }}">{{ message }}</div>
    {% endif %}
    
    <div class="stats">
        <div class="stat-item">
            <span>Saldo:</span>
            <span class="stat-value">${{ "%.2f"|format(saldo) }}</span>
        </div>
        <div class="stat-item">
            <span>Depósito Inicial:</span>
            <span class="stat-value">${{ "%.2f"|format(deposito_inicial) }}</span>
        </div>
        <div class="stat-item">
            <span>Valor del Portafolio:</span>
            <span class="stat-value">${{ "%.2f"|format(valor_portafolio) }}</span>
        </div>
        <div class="stat-item">
            <span>Ganancia/Pérdida:</span>
            <span class="stat-value" style="color: {{ ganancia_perdida_color }}">${{ "%.2f"|format(ganancia_perdida) }}</span>
        </div>
    </div>
    
    <div class="container">
        <div class="panel">
            <h2>Operaciones</h2>
            
            <div class="form-group">
                <label>Depositar fondos</label>
                <form method="POST" action="/depositar">
                    <input type="number" name="monto" step="0.01" placeholder="Monto" required>
                    <button type="submit" class="deposit">Depositar</button>
                </form>
            </div>
            
            <div class="form-group">
                <label>Retirar fondos</label>
                <form method="POST" action="/retirar">
                    <input type="number" name="monto" step="0.01" placeholder="Monto" required>
                    <button type="submit" class="withdraw">Retirar</button>
                </form>
            </div>
            
            <h3>Comprar Venta de Acciones</h3>
            
            <div class="form-group">
                <label>Comprar acciones</label>
                <form method="POST" action="/comprar">
                    <input type="text" name="simbolo" placeholder="Símbolo (AAPL, TSLA, GOOGL)" required>
                    <input type="number" name="cantidad" min="1" placeholder="Cantidad" required>
                    <button type="submit" class="buy">Comprar</button>
                </form>
            </div>
            
            <div class="form-group">
                <label>Vender acciones</label>
                <form method="POST" action="/vender">
                    <input type="text" name="simbolo" placeholder="Símbolo (AAPL, TSLA, GOOGL)" required>
                    <input type="number" name="cantidad" min="1" placeholder="Cantidad" required>
                    <button type="submit" class="sell">Vender</button>
                </form>
            </div>
        </div>
        
        <div class="panel">
            <h2>Información de la Cuenta</h2>
            
            <div class="form-group">
                <h3>Tenencias Actuales</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Símbolo</th>
                            <th>Cantidad</th>
                            <th>Precio</th>
                            <th>Valor</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for simbolo, cantidad in tenencias.items() %}
                        <tr>
                            <td>{{ simbolo }}</td>
                            <td>{{ cantidad }}</td>
                            <td>${{ "%.2f"|format(get_share_pryce(simbolo)) }}</td>
                            <td>${{ "%.2f"|format(get_share_pryce(simbolo) * cantidad) }}</td>
                        </tr>
                        {% else %}
                        <tr>
                            <td colspan="4">No posee acciones</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    
    <div class="panel">
        <h2>Historial de Transacciones</h2>
        <table>
            <thead>
                <tr>
                    <th>Fecha</th>
                    <th>Tipo</th>
                    <th>Detalles</th>
                </tr>
            </thead>
            <tbody>
                {% for transaccion in transacciones %}
                <tr>
                    <td>{{ transaccion.timestamp | strftime }}</td>
                    <td>{{ transaccion.tipo }}</td>
                    <td>
                        {% if transaccion.tipo == "DEPOSITO" %}
                        Depósito: ${{ "%.2f"|format(transaccion.detalle.monto) }}
                        {% elif transaccion.tipo == "RETIRO" %}
                        Retiro: ${{ "%.2f"|format(transaccion.detalle.monto) }}
                        {% elif transaccion.tipo == "COMPRA" %}
                        Compra: {{ transaccion.detalle.cantidad }} x {{ transaccion.detalle.simbolo }} @ ${{ "%.2f"|format(transaccion.detalle.precio_unitario) }} = ${{ "%.2f"|format(transaccion.detalle.costo_total) }}
                        {% elif transaccion.tipo == "VENTA" %}
                        Venta: {{ transaccion.detalle.cantidad }} x {{ transaccion.detalle.simbolo }} @ ${{ "%.2f"|format(transaccion.detalle.precio_unitario) }} = ${{ "%.2f"|format(transaccion.detalle.ingreso_total) }}
                        {% else %}
                        {{ transaccion.detalle }}
                        {% endif %}
                    </td>
                </tr>
                {% else %}
                <tr>
                    <td colspan="3">No hay transacciones aún</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>
'''

@app.template_filter('strftime')
def strftime_filter(timestamp):
    """Formatear timestamp a fecha legible."""
    import datetime
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

@app.route('/')
def index():
    """Mostrar la página principal con la información de la cuenta."""
    try:
        saldo = cuenta.saldo
        deposito_inicial = cuenta.deposito_inicial
        valor_portafolio = cuenta.valor_portafolio()
        ganancia_perdida = cuenta.ganancia_perdida()
        tenencias = cuenta.tenencias()
        transacciones = cuenta.transacciones()
        
        # Determinar color para ganancia/pérdida
        if ganancia_perdida > 0:
            ganancia_perdida_color = "green"
        elif ganancia_perdida < 0:
            ganancia_perdida_color = "red"
        else:
            ganancia_perdida_color = "black"
        
        return render_template_string(
            HTML_TEMPLATE,
            saldo=saldo,
            deposito_inicial=deposito_inicial,
            valor_portafolio=valor_portafolio,
            ganancia_perdida=ganancia_perdida,
            ganancia_perdida_color=ganancia_perdida_color,
            tenencias=tenencias,
            transacciones=transacciones,
            message=None,
            message_type=None
        )
    except Exception as e:
        return render_template_string(HTML_TEMPLATE, 
                                     message=f"Error: {str(e)}",
                                     message_type="error",
                                     saldo=0,
                                     deposito_inicial=0,
                                     valor_portafolio=0,
                                     ganancia_perdida=0,
                                     ganancia_perdida_color="black",
                                     tenencias={},
                                     transacciones=[])

@app.route('/depositar', methods=['POST'])
def depositar():
    """Procesar un depósito."""
    try:
        monto = float(request.form['monto'])
        cuenta.depositar(monto)
        return index()
    except ValueError as e:
        return render_template_string(HTML_TEMPLATE, 
                                     message=str(e),
                                     message_type="error",
                                     saldo=cuenta.saldo,
                                     deposito_inicial=cuenta.deposito_inicial,
                                     valor_portafolio=cuenta.valor_portafolio(),
                                     ganancia_perdida=cuenta.ganancia_perdida(),
                                     ganancia_perdida_color="black" if cuenta.ganancia_perdida() == 0 else ("green" if cuenta.ganancia_perdida() > 0 else "red"),
                                     tenencias=cuenta.tenencias(),
                                     transacciones=cuenta.transacciones())

@app.route('/retirar', methods=['POST'])
def retirar():
    """Procesar un retiro."""
    try:
        monto = float(request.form['monto'])
        cuenta.retirar(monto)
        return index()
    except ValueError as e:
        return render_template_string(HTML_TEMPLATE, 
                                     message=str(e),
                                     message_type="error",
                                     saldo=cuenta.saldo,
                                     deposito_inicial=cuenta.deposito_inicial,
                                     valor_portafolio=cuenta.valor_portafolio(),
                                     ganancia_perdida=cuenta.ganancia_perdida(),
                                     ganancia_perdida_color="black" if cuenta.ganancia_perdida() == 0 else ("green" if cuenta.ganancia_perdida() > 0 else "red"),
                                     tenencias=cuenta.tenencias(),
                                     transacciones=cuenta.transacciones())

@app.route('/comprar', methods=['POST'])
def comprar():
    """Procesar una compra de acciones."""
    try:
        simbolo = request.form['simbolo'].upper()
        cantidad = int(request.form['cantidad'])
        cuenta.comprar_accion(simbolo, cantidad)
        return index()
    except ValueError as e:
        return render_template_string(HTML_TEMPLATE, 
                                     message=str(e),
                                     message_type="error",
                                     saldo=cuenta.saldo,
                                     deposito_inicial=cuenta.deposito_inicial,
                                     valor_portafolio=cuenta.valor_portafolio(),
                                     ganancia_perdida=cuenta.ganancia_perdida(),
                                     ganancia_perdida_color="black" if cuenta.ganancia_perdida() == 0 else ("green" if cuenta.ganancia_perdida() > 0 else "red"),
                                     tenencias=cuenta.tenencias(),
                                     transacciones=cuenta.transacciones())

@app.route('/vender', methods=['POST'])
def vender():
    """Procesar una venta de acciones."""
    try:
        simbolo = request.form['simbolo'].upper()
        cantidad = int(request.form['cantidad'])
        cuenta.vender_accion(simbolo, cantidad)
        return index()
    except ValueError as e:
        return render_template_string(HTML_TEMPLATE, 
                                     message=str(e),
                                     message_type="error",
                                     saldo=cuenta.saldo,
                                     deposito_inicial=cuenta.deposito_inicial,
                                     valor_portafolio=cuenta.valor_portafolio(),
                                     ganancia_perdida=cuenta.ganancia_perdida(),
                                     ganancia_perdida_color="black" if cuenta.ganancia_perdida() == 0 else ("green" if cuenta.ganancia_perdida() > 0 else "red"),
                                     tenencias=cuenta.tenencias(),
                                     transacciones=cuenta.transacciones())

if __name__ == '__main__':
    app.run(debug=True, port=5000)