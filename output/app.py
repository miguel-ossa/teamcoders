from flask import Flask, request, redirect, url_for, render_template_string, flash
from cuentas import Cuenta, get_share_price

app = Flask(__name__)
app.secret_key = "clave-secreta-demo"  # Necesario para mensajes flash

cuenta = None  # Solo un usuario, inicialmente sin cuenta


INDEX_HTML = """
<!doctype html>
<title>Simulación de Trading - Gestión de Cuenta</title>
<h1>Simulación de Trading - Gestión de Cuenta</h1>
{% with messages = get_flashed_messages() %}
  {% if messages %}
    <ul style="color:red;">
    {% for message in messages %}
      <li>{{ message }}</li>
    {% endfor %}
    </ul>
  {% endif %}
{% endwith %}

{% if cuenta is none %}
  <h2>Crear Cuenta</h2>
  <form method="post" action="{{ url_for('crear_cuenta') }}">
    <button type="submit">Crear nueva cuenta</button>
  </form>
{% else %}
  <h2>Estado de la Cuenta</h2>
  <p><b>Saldo efectivo:</b> {{ saldo_efectivo }} USD</p>
  <p><b>Valor total portafolio:</b> {{ valor_portafolio }} USD</p>
  <p><b>Ganancias/Perdidas:</b> {{ ganancia_perdida }} USD</p>

  <h3>Tenencias actuales</h3>
  {% if tenencias %}
    <ul>
    {% for simbolo, cantidad in tenencias.items() %}
      <li>{{ simbolo }} : {{ cantidad }} acciones (Precio actual: {{ precios[simbolo] }} USD)</li>
    {% endfor %}
    </ul>
  {% else %}
    <p>No posee acciones actualmente.</p>
  {% endif %}

  <h3>Operaciones</h3>
  <h4>Depositar fondos</h4>
  <form method="post" action="{{ url_for('depositar') }}">
    Monto a depositar (USD): <input type="number" step="0.01" name="monto" required>
    <button type="submit">Depositar</button>
  </form>

  <h4>Retirar fondos</h4>
  <form method="post" action="{{ url_for('retirar') }}">
    Monto a retirar (USD): <input type="number" step="0.01" name="monto" required>
    <button type="submit">Retirar</button>
  </form>

  <h4>Comprar acciones</h4>
  <form method="post" action="{{ url_for('comprar_acciones') }}">
    Símbolo (AAPL, TSLA, GOOGL): 
    <select name="simbolo" required>
      <option value="AAPL">AAPL</option>
      <option value="TSLA">TSLA</option>
      <option value="GOOGL">GOOGL</option>
    </select>
    Cantidad: <input type="number" name="cantidad" min="1" required>
    <button type="submit">Comprar</button>
  </form>

  <h4>Vender acciones</h4>
  <form method="post" action="{{ url_for('vender_acciones') }}">
    Símbolo:
    <select name="simbolo" required>
      {% for simbolo in tenencias.keys() %}
        <option value="{{ simbolo }}">{{ simbolo }}</option>
      {% endfor %}
    </select>
    Cantidad: <input type="number" name="cantidad" min="1" required>
    <button type="submit">Vender</button>
  </form>

  <h3>Historial de transacciones</h3>
  {% if transacciones %}
    <table border="1" cellpadding="5" cellspacing="0">
      <thead>
        <tr>
          <th>Fecha</th>
          <th>Tipo</th>
          <th>Símbolo</th>
          <th>Cantidad</th>
          <th>Precio Unitario</th>
        </tr>
      </thead>
      <tbody>
      {% for t in transacciones %}
        <tr>
          <td>{{ t.fecha }}</td>
          <td>{{ t.tipo }}</td>
          <td>{{ t.simbolo if 'simbolo' in t else '-' }}</td>
          <td>{{ t.cantidad if 'cantidad' in t else '-' }}</td>
          <td>{{ t.precio_unitario if 'precio_unitario' in t else '-' }}</td>
        </tr>
      {% endfor %}
      </tbody>
    </table>
  {% else %}
    <p>No se registraron transacciones aún.</p>
  {% endif %}

  <form method="post" action="{{ url_for('resetear_cuenta') }}">
    <button type="submit" style="margin-top: 20px;">Resetear Cuenta (borrar todo y crear nueva)</button>
  </form>
{% endif %}
"""


@app.route("/", methods=["GET"])
def index():
    global cuenta
    if cuenta is None:
        # No hay cuenta creada
        return render_template_string(INDEX_HTML, cuenta=None)
    else:
        try:
            tenencias = cuenta.obtener_tenencias()
            precios = {s: get_share_price(s) for s in tenencias.keys()}
            transacciones_raw = cuenta.listar_transacciones()
            # Adaptar formato fechas y claves para mejor visualización
            transacciones = []
            for tr in transacciones_raw:
                transacciones.append({
                    "fecha": tr.get("fecha", ""),
                    "tipo": tr.get("tipo", ""),
                    "simbolo": tr.get("simbolo", None),
                    "cantidad": tr.get("cantidad", None),
                    "precio_unitario": tr.get("precio_unitario", None)
                })
            return render_template_string(
                INDEX_HTML,
                cuenta=cuenta,
                saldo_efectivo=f"{cuenta._saldo_efectivo:.2f}",
                valor_portafolio=f"{cuenta.valor_portafolio():.2f}",
                ganancia_perdida=f"{cuenta.ganancias_perdidas():.2f}",
                tenencias=tenencias,
                precios=precios,
                transacciones=transacciones,
            )
        except Exception as e:
            flash(f"Error al cargar datos de la cuenta: {str(e)}")
            return render_template_string(INDEX_HTML, cuenta=cuenta)


@app.route("/crear", methods=["POST"])
def crear_cuenta():
    global cuenta
    cuenta = Cuenta()
    flash("Cuenta creada exitosamente.")
    return redirect(url_for("index"))


@app.route("/depositar", methods=["POST"])
def depositar():
    global cuenta
    if cuenta is None:
        flash("Primero cree una cuenta.")
        return redirect(url_for("index"))
    try:
        monto = float(request.form.get("monto", "0"))
        cuenta.depositar(monto)
        flash(f"Depósito de {monto:.2f} USD realizado.")
    except Exception as e:
        flash(f"Error al depositar: {str(e)}")
    return redirect(url_for("index"))


@app.route("/retirar", methods=["POST"])
def retirar():
    global cuenta
    if cuenta is None:
        flash("Primero cree una cuenta.")
        return redirect(url_for("index"))
    try:
        monto = float(request.form.get("monto", "0"))
        cuenta.retirar(monto)
        flash(f"Retiro de {monto:.2f} USD realizado.")
    except Exception as e:
        flash(f"Error al retirar: {str(e)}")
    return redirect(url_for("index"))


@app.route("/comprar", methods=["POST"])
def comprar_acciones():
    global cuenta
    if cuenta is None:
        flash("Primero cree una cuenta.")
        return redirect(url_for("index"))
    try:
        simbolo = request.form.get("simbolo", "")
        cantidad = int(request.form.get("cantidad", "0"))
        cuenta.comprar_acciones(simbolo, cantidad)
        flash(f"Compra de {cantidad} acciones de {simbolo} realizada.")
    except Exception as e:
        flash(f"Error al comprar acciones: {str(e)}")
    return redirect(url_for("index"))


@app.route("/vender", methods=["POST"])
def vender_acciones():
    global cuenta
    if cuenta is None:
        flash("Primero cree una cuenta.")
        return redirect(url_for("index"))
    try:
        simbolo = request.form.get("simbolo", "")
        cantidad = int(request.form.get("cantidad", "0"))
        cuenta.vender_acciones(simbolo, cantidad)
        flash(f"Venta de {cantidad} acciones de {simbolo} realizada.")
    except Exception as e:
        flash(f"Error al vender acciones: {str(e)}")
    return redirect(url_for("index"))


@app.route("/reset", methods=["POST"])
def resetear_cuenta():
    global cuenta
    cuenta = None
    flash("Cuenta reseteada.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)