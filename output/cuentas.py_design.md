```markdown
# Diseño del módulo `cuentas.py`

El módulo `cuentas.py` implementa un sistema de gestión de cuentas para una plataforma de simulación de trading. La clase principal es `Cuenta`, que maneja el saldo, las tenencias de acciones, las transacciones y cálculos financieros.

---

## Clase `Cuenta`

### Atributos
- `balance`: `float` - Saldo disponible en la cuenta.
- `initial_deposit`: `float` - Monto inicial depositado por el usuario.
- `holdings`: `Dict[str, Dict[str, Union[int, float]]]` - Diccionario de tenencias de acciones. La clave es el símbolo de la acción, y el valor es otro diccionario con:
  - `"quantity"`: `int` - Cantidad de acciones poseídas.
  - `"cost_basis"`: `float` - Costo total de adquisición de las acciones.
- `transactions`: `List[Dict[str, Union[str, int, float, datetime]]]` - Historial de transacciones. Cada entrada incluye:
  - `"type"`: `str` - Tipo de transacción (`"deposit"`, `"withdraw"`, `"buy"`, `"sell"`).
  - `"symbol"`: `str` - Símbolo de la acción (aplica solo para transacciones de compra/venta).
  - `"quantity"`: `int` - Cantidad de acciones o monto en efectivo.
  - `"price"`: `float` - Precio unitario (aplica para transacciones de compra/venta).
  - `"timestamp"`: `datetime` - Fecha y hora de la transacción.
  - `"balance"`: `float` - Saldo después de la transacción.

---

### Métodos

#### `__init__(self, initial_deposit: float)`
- **Descripción**: Inicializa una nueva cuenta con un depósito inicial.
- **Parámetros**:
  - `initial_deposit`: Monto inicial depositado.
- **Excepciones**: Lanza `ValueError` si `initial_deposit` es negativo o cero.

---

#### `deposit(self, amount: float) -> None`
- **Descripción**: Añade fondos a la cuenta.
- **Parámetros**:
  - `amount`: Monto a depositar.
- **Excepciones**: Lanza `ValueError` si `amount` es negativo o cero.

---

#### `withdraw(self, amount: float) -> None`
- **Descripción**: Retira fondos de la cuenta, asegurando que el saldo no se vuelva negativo.
- **Parámetros**:
  - `amount`: Monto a retirar.
- **Excepciones**:
  - `ValueError` si `amount` es negativo o cero.
  - `ValueError` si el retiro dejaría el saldo negativo.

---

#### `buy_stock(self, symbol: str, quantity: int) -> None`
- **Descripción**: Compra acciones de un símbolo dado, verificando que el usuario tenga fondos suficientes.
- **Parámetros**:
  - `symbol`: Símbolo de la acción (ej: `"AAPL"`).
  - `quantity`: Cantidad de acciones a comprar.
- **Excepciones**:
  - `ValueError` si `quantity` es menor o igual a cero.
  - `ValueError` si el precio de la acción multiplicado por la cantidad excede el saldo disponible.

---

#### `sell_stock(self, symbol: str, quantity: int) -> None`
- **Descripción**: Vende acciones de un símbolo dado, verificando que el usuario posea la cantidad solicitada.
- **Parámetros**:
  - `symbol`: Símbolo de la acción.
  - `quantity`: Cantidad de acciones a vender.
- **Excepciones**:
  - `ValueError` si `quantity` es menor o igual a cero.
  - `ValueError` si el usuario no posee la cantidad solicitada de acciones.

---

#### `get_portfolio_value(self) -> float`
- **Descripción**: Calcula el valor total del portafolio (saldo + valor de las acciones en posesión).
- **Retorno**: `float` - Valor total del portafolio.

---

#### `get_profit_loss(self) -> float`
- **Descripción**: Calcula las ganancias o pérdidas respecto al depósito inicial.
- **Retorno**: `float` - Ganancias (positivo) o pérdidas (negativo).

---

#### `get_holdings(self) -> Dict[str, Dict[str, Union[int, float]]]`
- **Descripción**: Devuelve el diccionario de tenencias de acciones.
- **Retorno**: `Dict[str, Dict[str, Union[int, float]]]` - Estructura descrita en los atributos.

---

#### `get_transactions(self) -> List[Dict[str, Union[str, int, float, datetime]]]`
- **Descripción**: Devuelve el historial completo de transacciones.
- **Retorno**: `List[Dict[...]]` - Lista de transacciones con detalles.

---

## Función `get_share_price(symbol: str) -> float`

### Descripción
- **Descripción**: Devuelve el precio actual de una acción según su símbolo.
- **Parámetros**:
  - `symbol`: Símbolo de la acción (ej: `"AAPL"`).
- **Retorno**: `float` - Precio de la acción.
- **Implementación de prueba**:
  - `AAPL`: 150.0
  - `TSLA`: 250.0
  - `GOOGL`: 130.0
  - Otros símbolos: `ValueError`

---

## Ejemplo de uso
```python
from cuentas import Cuenta, get_share_price

cuenta = Cuenta(initial_deposit=10000)
cuenta.buy_stock("AAPL", 20)
cuenta.sell_stock("AAPL", 5)
print(cuenta.get_portfolio_value())
print(cuenta.get_profit_loss())
print(cuenta.get_transactions())
```

---

## Consideraciones
- El módulo es autónomo y no depende de otras bibliotecas (excepto `datetime` para timestamps).
- Todas las validaciones se manejan mediante `ValueError`.
- La función `get_share_price` se puede reemplazar con una implementación real en producción.
```