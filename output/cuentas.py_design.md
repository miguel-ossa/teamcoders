# Diseño del módulo `cuentas.py`

## Clase `Cuenta`
La clase `Cuenta` representa una cuenta de usuario en el sistema de gestión de cuentas para la plataforma de simulación de trading. Incluye métodos para gestionar saldos, transacciones, portafolio y cálculos de ganancias/pérdidas.

### Atributos
- `saldo_inicial`: El valor del depósito inicial del usuario (float).
- `saldo_actual`: El saldo actual de la cuenta (float).
- `portafolio`: Un diccionario que mapea símbolos de acciones a la cantidad poseída (dict[str, int]).
- `transacciones`: Una lista de transacciones registradas (list[dict]).

### Métodos

#### `__init__(self, saldo_inicial: float)`
- **Descripción**: Inicializa una nueva cuenta con un saldo inicial especificado. 
- **Validación**: El `saldo_inicial` debe ser un valor numérico positivo.
- **Ejemplo**:
  ```python
  cuenta = Cuenta(10000.0)
  ```

#### `depositar(self, monto: float) -> None`
- **Descripción**: Agrega un monto al saldo actual de la cuenta.
- **Validación**: El `monto` debe ser un valor numérico positivo.
- **Ejemplo**:
  ```python
  cuenta.depositar(5000.0)
  ```

#### `retirar(self, monto: float) -> None`
- **Descripción**: Resta un monto del saldo actual, siempre que el saldo no se vuelva negativo.
- **Validación**: El `monto` debe ser positivo y no mayor que el `saldo_actual`.
- **Ejemplo**:
  ```python
  cuenta.retirar(2000.0)
  ```

#### `comprar_acciones(self, simbolo: str, cantidad: int) -> None`
- **Descripción**: Permite al usuario comprar acciones de un símbolo específico, verificando que el monto total (precio * cantidad) sea cubierto por el `saldo_actual`.
- **Validación**: 
  - `simbolo` debe ser una cadena no vacía.
  - `cantidad` debe ser un entero positivo.
  - El precio de las acciones multiplicado por `cantidad` no debe exceder el `saldo_actual`.
- **Ejemplo**:
  ```python
  cuenta.comprar_acciones('AAPL', 10)
  ```

#### `vender_acciones(self, simbolo: str, cantidad: int) -> None`
- **Descripción**: Permite al usuario vender acciones de un símbolo específico, verificando que posea la cantidad solicitada.
- **Validación**: 
  - `simbolo` debe ser una cadena no vacía.
  - `cantidad` debe ser un entero positivo.
  - El usuario debe poseer al menos `cantidad` de acciones del símbolo.
- **Ejemplo**:
  ```python
  cuenta.vender_acciones('AAPL', 5)
  ```

#### `calcular_valor_total(self) -> float`
- **Descripción**: Calcula el valor total del portafolio del usuario basado en los precios actuales de las acciones.
- **Ejemplo**:
  ```python
  valor_total = cuenta.calcular_valor_total()
  ```

#### `calcular_ganancias_perdidas(self) -> float`
- **Descripción**: Calcula las ganancias o pérdidas del usuario comparando el valor total del portafolio con el `saldo_inicial`.
- **Ejemplo**:
  ```python
  ganancias = cuenta.calcular_ganancias_perdidas()
  ```

#### `get_tenencias(self) -> dict[str, int]`
- **Descripción**: Retorna una copia del portafolio actual del usuario.
- **Ejemplo**:
  ```python
  tenencias = cuenta.get_tenencias()
  ```

#### `listar_transacciones(self) -> list[dict]`
- **Descripción**: Retorna una lista de todas las transacciones realizadas por el usuario.
- **Ejemplo**:
  ```python
  transacciones = cuenta.listar_transacciones()
  ```

---

## Función `get_share_price(symbol: str) -> float`
- **Descripción**: Retorna el precio actual de una acción de un símbolo específico. 
- **Implementación de prueba**: Devuelve precios fijos para los símbolos `AAPL`, `TSLA`, y `GOOGL`. Para otros símbolos, devuelve `0.0`.
- **Ejemplo**:
  ```python
  precio = get_share_price('AAPL')  # Devuelve 150.0
  ```

---

## Estructura del módulo

```python
# cuentas.py

def get_share_price(symbol: str) -> float:
    test_prices = {
        'AAPL': 150.0,
        'TSLA': 250.0,
        'GOOGL': 130.0
    }
    return test_prices.get(symbol, 0.0)

class Cuenta:
    def __init__(self, saldo_inicial: float):
        # Inicializa los atributos
        pass

    def depositar(self, monto: float) -> None:
        # Lógica para depositar
        pass

    def retirar(self, monto: float) -> None:
        # Lógica para retirar
        pass

    def comprar_acciones(self, simbolo: str, cantidad: int) -> None:
        # Lógica para comprar
        pass

    def vender_acciones(self, simbolo: str, cantidad: int) -> None:
        # Lógica para vender
        pass

    def calcular_valor_total(self) -> float:
        # Cálculo del valor total
        pass

    def calcular_ganancias_perdidas(self) -> float:
        # Cálculo de ganancias o pérdidas
        pass

    def get_tenencias(self) -> dict[str, int]:
        # Retorna el portafolio
        pass

    def listar_transacciones(self) -> list[dict]:
        # Retorna las transacciones
        pass
```

---

## Notas
- El módulo es autónomo y puede ser probado directamente.
- El método `get_share_price` es utilizado internamente por `comprar_acciones` y `vender_acciones` para obtener precios de acciones.
- La validación de entradas (ej. tipos incorrectos, valores negativos) se deja como responsabilidad del desarrollador, pero debe implementarse en la lógica de los métodos.