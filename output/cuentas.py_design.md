# Diseño del módulo `cuentas.py`

## Clase: `Cuenta`

### Atributos
- `saldo`: `float` - Saldo actual de la cuenta.
- `portafolio`: `Dict[str, int]` - Diccionario que mapea símbolos de acciones a la cantidad poseída.
- `deposito_inicial`: `float` - Valor del depósito inicial realizado por el usuario.
- `transacciones`: `List[Dict[str, Any]]` - Lista de todas las transacciones realizadas por el usuario.

---

### Métodos

#### `__init__(self, deposito_inicial: float)`
- **Descripción**: Inicializa una nueva cuenta con un depósito inicial.
- **Validaciones**:
  - `deposito_inicial` debe ser un número positivo.
- **Ejemplo**:
  ```python
  cuenta = Cuenta(deposito_inicial=10000.0)
  ```

---

#### `depositar(self, monto: float) -> None`
- **Descripción**: Añade fondos a la cuenta.
- **Validaciones**:
  - `monto` debe ser un número positivo.
- **Efectos secundarios**:
  - Aumenta el `saldo` en `monto`.
  - Registra una transacción de tipo `"deposito"` en `transacciones`.

---

#### `retirar(self, monto: float) -> None`
- **Descripción**: Retira fondos de la cuenta.
- **Validaciones**:
  - `monto` debe ser un número positivo.
  - El `saldo` no puede ser menor a cero después de la operación.
- **Efectos secundarios**:
  - Disminuye el `saldo` en `monto`.
  - Registra una transacción de tipo `"retiro"` en `transacciones`.

---

#### `comprar(self, simbolo: str, cantidad: int) -> None`
- **Descripción**: Compra una cantidad específica de acciones de un símbolo.
- **Validaciones**:
  - `simbolo` debe ser una cadena no vacía.
  - `cantidad` debe ser un entero positivo.
  - El costo total (`cantidad * get_share_price(simbolo)`) no puede exceder el `saldo`.
- **Efectos secundarios**:
  - Disminuye el `saldo` en el costo total de la compra.
  - Aumenta la cantidad en `portafolio` para el `simbolo`.
  - Registra una transacción de tipo `"compra"` en `transacciones`.

---

#### `vender(self, simbolo: str, cantidad: int) -> None`
- **Descripción**: Vende una cantidad específica de acciones de un símbolo.
- **Validaciones**:
  - `simbolo` debe ser una cadena no vacía.
  - `cantidad` debe ser un entero positivo.
  - El usuario debe poseer al menos `cantidad` de acciones del `simbolo`.
- **Efectos secundarios**:
  - Aumenta el `saldo` en el valor de la venta (`cantidad * get_share_price(simbolo)`).
  - Disminuye la cantidad en `portafolio` para el `simbolo`.
  - Registra una transacción de tipo `"venta"` en `transacciones`.

---

#### `valor_total_portafolio(self) -> float`
- **Descripción**: Calcula el valor total del portafolio actual.
- **Lógica**:
  - Suma el valor de todas las acciones en `portafolio` usando `get_share_price(simbolo)`.
- **Retorno**:
  - Valor total del portafolio como `float`.

---

#### `ganancias_o_perdidas(self) -> float`
- **Descripción**: Calcula las ganancias o pérdidas respecto al depósito inicial.
- **Lógica**:
  - `valor_total_portafolio()` - `deposito_inicial`.
- **Retorno**:
  - Valor de ganancias o pérdidas como `float`.

---

#### `obtener_tenencias(self) -> Dict[str, int]`
- **Descripción**: Devuelve el estado actual del portafolio.
- **Retorno**:
  - Copia del diccionario `portafolio`.

---

#### `obtener_transacciones(self) -> List[Dict[str, Any]]`
- **Descripción**: Devuelve una lista de todas las transacciones realizadas.
- **Retorno**:
  - Copia de la lista `transacciones`.

---

## Función Auxiliar: `get_share_price(symbol: str) -> float`

### Descripción
- **Función de prueba** que devuelve precios fijos para los símbolos `AAPL`, `TSLA` y `GOOGL`.
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

### Uso
- La función se usa en métodos como `comprar()` y `vender()` para determinar el precio actual de las acciones.

---

## Ejemplo de Uso
```python
from cuentas import Cuenta, get_share_price

cuenta = Cuenta(deposito_inicial=10000.0)
cuenta.comprar("AAPL", 50)  # Compra 50 acciones de AAPL
print(cuenta.valor_total_portafolio())  # Calcula el valor total del portafolio
print(cuenta.ganancias_o_perdidas())  # Calcula ganancias o pérdidas
print(cuenta.obtener_tenencias())  # Muestra las tenencias actuales
print(cuenta.obtener_transacciones())  # Muestra todas las transacciones
```

---

## Notas
- El módulo es completamente autónomo y no depende de otros módulos externos.
- Las validaciones garantizan que no se permitan operaciones ilegales (ej: vender acciones que no se poseen).