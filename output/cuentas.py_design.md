# Diseño del módulo `cuentas.py`

## Clase `Cuenta`

La clase `Cuenta` representa una cuenta de usuario en el sistema de gestión de cuentas para una plataforma de simulación de trading. Gestiona el saldo, las tenencias de acciones, las transacciones realizadas y calcula métricas del portafolio.

### Atributos de la clase

- **usuario**: `str` - El nombre de usuario asociado a la cuenta.
- **saldo**: `float` - El saldo actual en la cuenta (dinero disponible).
- **tenencias**: `Dict[str, int]` - Un diccionario que mapea símbolos de acciones a la cantidad poseída por el usuario.
- **transacciones**: `List[Dict[str, Any]]` - Una lista de transacciones realizadas, cada una representada como un diccionario con los campos: `tipo` (compra/venta), `simbolo`, `cantidad`, `precio`, `timestamp`.
- **deposito_inicial**: `float` - El monto inicial depositado cuando se creó la cuenta.

---

### Métodos de la clase

#### `__init__(self, usuario: str, deposito_inicial: float)`

- **Descripción**: Inicializa una nueva cuenta con el nombre de usuario y el depósito inicial especificado.
- **Precondiciones**:
  - `deposito_inicial` debe ser un valor numérico positivo.
- **Postcondiciones**:
  - `saldo` se inicializa con `deposito_inicial`.
  - `deposito_inicial` se almacena como atributo.
  - `tenencias` se inicializa como un diccionario vacío.
  - `transacciones` se inicializa como una lista vacía.

---

#### `depositar(self, monto: float) -> None`

- **Descripción**: Añade un monto al saldo de la cuenta.
- **Precondiciones**:
  - `monto` debe ser un valor numérico positivo.
- **Postcondiciones**:
  - El `saldo` se incrementa en `monto`.
  - Se registra una transacción de tipo "depósito" (no se requiere en el requisito, pero se incluye para extensión futura).

---

#### `retirar(self, monto: float) -> None`

- **Descripción**: Resta un monto del saldo de la cuenta, siempre que no deje el saldo negativo.
- **Precondiciones**:
  - `monto` debe ser un valor numérico positivo.
  - El `saldo` actual debe ser mayor o igual a `monto` después de la operación.
- **Postcondiciones**:
  - El `saldo` se decrementa en `monto`.
  - Se registra una transacción de tipo "retiro" (no se requiere en el requisito, pero se incluye para extensión futura).

---

#### `comprar_acciones(self, simbolo: str, cantidad: int) -> None`

- **Descripción**: Permite al usuario comprar una cantidad específica de acciones de un símbolo dado, usando el precio actual obtenido por `get_share_price`.
- **Precondiciones**:
  - `simbolo` debe ser una cadena válida (ej. "AAPL").
  - `cantidad` debe ser un número entero positivo.
  - El `saldo` debe ser suficiente para pagar el costo total de la compra (`cantidad * precio`).
- **Postcondiciones**:
  - El `saldo` se decrementa en el costo total de la compra.
  - `tenencias[simbolo]` se incrementa en `cantidad`.
  - Se registra una transacción de tipo "compra" con el precio actual del símbolo.

---

#### `vender_acciones(self, simbolo: str, cantidad: int) -> None`

- **Descripción**: Permite al usuario vender una cantidad específica de acciones de un símbolo dado, usando el precio actual obtenido por `get_share_price`.
- **Precondiciones**:
  - `simbolo` debe ser una cadena válida (ej. "AAPL").
  - `cantidad` debe ser un número entero positivo.
  - El usuario debe poseer al menos `cantidad` de acciones del símbolo especificado.
- **Postcondiciones**:
  - `tenencias[simbolo]` se decrementa en `cantidad`.
  - El `saldo` se incrementa en el valor de la venta (`cantidad * precio`).
  - Se registra una transacción de tipo "venta" con el precio actual del símbolo.

---

#### `calcular_valor_total(self) -> float`

- **Descripción**: Calcula el valor total del portafolio del usuario, que incluye el saldo actual y el valor de mercado de todas las tenencias.
- **Retorno**: `float` - Valor total del portafolio.
- **Lógica**:
  - Para cada símbolo en `tenencias`, se multiplica `cantidad` por `get_share_price(simbolo)`.
  - Se suma el total de los valores de mercado y el `saldo`.

---

#### `calcular_ganancias_perdidas(self) -> float`

- **Descripción**: Calcula las ganancias o pérdidas del usuario respecto al depósito inicial.
- **Retorno**: `float` - Ganancias (positivo) o pérdidas (negativo).
- **Lógica**:
  - Valor total actual del portafolio - `deposito_inicial`.

---

#### `obtener_tenencias(self) -> Dict[str, int]`

- **Descripción**: Devuelve el diccionario que representa las tenencias actuales del usuario.
- **Retorno**: `Dict[str, int]` - Símbolos como claves y cantidades como valores.

---

#### `listar_transacciones(self) -> List[Dict[str, Any]]`

- **Descripción**: Devuelve la lista completa de transacciones realizadas por el usuario.
- **Retorno**: `List[Dict[str, Any]]` - Cada transacción incluye: `tipo`, `simbolo`, `cantidad`, `precio`, `timestamp`.

---

### Función auxiliar `_registrar_transaccion(self, tipo: str, simbolo: str, cantidad: int, precio: float) -> None`

- **Descripción**: Registra una nueva transacción en `transacciones`.
- **Parámetros**:
  - `tipo`: "compra" o "venta".
  - `simbolo`: Símbolo de la acción.
  - `cantidad`: Cantidad comprada o vendida.
  - `precio`: Precio de la acción en el momento de la transacción.
- **Postcondiciones**:
  - Se agrega un nuevo diccionario a `transacciones` con los parámetros proporcionados y un `timestamp` actual (usando `datetime.now()`).

---

## Función externa `get_share_price(symbol: str) -> float`

- **Descripción**: Devuelve el precio actual de una acción según el símbolo proporcionado.
- **Implementación de prueba**:
  ```python
  def get_share_price(symbol: str) -> float:
      precios_prueba = {
          "AAPL": 190.0,
          "TSLA": 260.0,
          "GOOGL": 135.0
      }
      return precios_prueba.get(symbol, 0.0)
  ```
- **Nota**: Esta función se incluye como parte del módulo para pruebas, pero puede reemplazarse en futuras implementaciones con una conexión a una API real.