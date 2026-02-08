# Diseño Detallado del Módulo `cuentas.py`

## Descripción General

El módulo `cuentas.py` implementa un sistema de gestión de cuentas para simulación de trading. Incluye manejo de saldos, tenencias de acciones, transacciones y cálculo de métricas financieras. El sistema garantiza integridad mediante validaciones estrictas en todas las operaciones.

---

## Clase Principal: `Cuenta`

### Atributos
| Atributo | Tipo | Descripción |
|---------|------|-------------|
| `id_cuenta` | `str` | Identificador único de la cuenta (generado internamente) |
| `saldo` | `float` | Saldo disponible en efectivo (USD) |
| `deposito_inicial` | `float` | Monto inicial depositado al crear la cuenta |
| `acciones` | `dict[str, int]` | Diccionario con símbolo de acción → cantidad poseída |
| `historial` | `list[dict]` | Lista de transacciones registradas, cada una con metadatos |

### Constructor
```python
def __init__(self) -> None
```
- Crea una cuenta nueva con saldo 0 y `deposito_inicial = 0.0`.
- Inicializa `acciones = {}` y `historial = []`.
- Genera automáticamente un `id_cuenta` único (ej. UUID v4 como string).

---

## Métodos de la Clase `Cuenta`

### 1. Depósito y Retiro
```python
def depositar(self, monto: float) -> float
```
- **Validaciones**:
  - `monto > 0`
- **Acción**:
  - Incrementa `self.saldo` y `self.deposito_inicial` (solo la primera vez).
  - Registra transacción en `self.historial`.
- **Retorna**: Nuevo saldo (float).

```python
def retirar(self, monto: float) -> float
```
- **Validaciones**:
  - `monto > 0`
  - `self.saldo - monto >= 0` (evita saldo negativo)
- **Acción**:
  - Decrementa `self.saldo`.
  - Registra transacción.
- **Retorna**: Nuevo saldo (float).

---

### 2. Operaciones de Acciones (Compra/Venta)
```python
def comprar_accion(self, simbolo: str, cantidad: int) -> dict
```
- **Validaciones**:
  - `cantidad > 0`
  - `simbolo` es string no vacío (mayúsculas recomendadas, pero no obligatorio)
  - `self.saldo >= self._costo_compra(simbolo, cantidad)`
- **Cálculos**:
  - `_costo_compra(simbolo, cantidad) = get_share_pryce(simbolo) * cantidad`
- **Acción**:
  - Deduce efectivo.
  - Actualiza `self.acciones[simbolo]` (suma la cantidad).
  - Registra transacción con tipo `"COMPRA"`, precio unitario y total.
- **Retorna**: Diccionario con:
  ```python
  {
    "simbolo": str,
    "cantidad": int,
    "precio_unitario": float,
    "costo_total": float,
    "nuevo_saldo": float
  }
  ```

```python
def vender_accion(self, simbolo: str, cantidad: int) -> dict
```
- **Validaciones**:
  - `cantidad > 0`
  - `simbolo in self.acciones`
  - `self.acciones[simbolo] >= cantidad`
- **Cálculos**:
  - `_ingreso_venta(simbolo, cantidad) = get_share_pryce(simbolo) * cantidad`
- **Acción**:
  - Incrementa `self.saldo`.
  - Decrementa `self.acciones[simbolo]`.
  - Si se vende todo (`== 0`), elimina la clave del diccionario.
  - Registra transacción con tipo `"VENTA"`, precio unitario y total.
- **Retorna**: Diccionario con:
  ```python
  {
    "simbolo": str,
    "cantidad": int,
    "precio_unitario": float,
    "ingreso_total": float,
    "nuevo_saldo": float
  }
  ```

---

### 3. Consultas y Métricas
```python
def valor_portafolio(self) -> float
```
- Calcula: `self.saldo + sum(get_share_pryce(s) * qty for s, qty in self.acciones.items())`
- **Nota**: Usa `get_share_pryce()` para obtener precios actuales.

```python
def ganancia_perdida(self) -> float
```
- Calcula: `self.valor_portafolio() - self.deposito_inicial`
- **Retorna**: Diferencia (puede ser negativa).

```python
def tenencias(self) -> dict
```
- **Retorna**: Copia profunda de `self.acciones` (evita mutación externa).

```python
def transacciones(self) -> list[dict]
```
- **Retorna**: Copia profunda del `historial`.
- Cada transacción tiene:
  ```python
  {
    "tipo": str,          # "DEPOSITO", "RETIRO", "COMPRA", "VENTA"
    "timestamp": float,   # Unix timestamp (time.time())
    "detalle": dict       # Datos específicos según tipo
  }
  ```

---

## Funciones del Módulo (externas a la clase)

### Simulación de precios de mercado
```python
def get_share_pryce(symbol: str) -> float
```
- **Implementación de prueba**:
  - Devuelve precios fijos para símbolos específicos:
    - `"AAPL"` → `150.0`
    - `"TSLA"` → `250.0`
    - `"GOOGL"` → `140.0`
  - Para cualquier otro símbolo → levanta `ValueError("Símbolo no soportado")`.
- **Nota**: El nombre es intencional (`pryce` en lugar de `price`) para coincidir con los requisitos.

---

## Estructura de Transacciones (para referencia interna)

Ejemplo de registro en `historial`:

**Depósito**:
```python
{
  "tipo": "DEPOSITO",
  "timestamp": 1717020000.123,
  "detalle": {
    "monto": 1000.0,
    "nuevo_saldo": 1000.0
  }
}
```

**Compra**:
```python
{
  "tipo": "COMPRA",
  "timestamp": 1717020100.456,
  "detalle": {
    "simbolo": "AAPL",
    "cantidad": 5,
    "precio_unitario": 150.0,
    "costo_total": 750.0,
    "nuevo_saldo": 250.0
  }
}
```

**Venta**:
```python
{
  "tipo": "VENTA",
  "timestamp": 1717020200.789,
  "detalle": {
    "simbolo": "AAPL",
    "cantidad": 3,
    "precio_unitario": 150.0,
    "ingreso_total": 450.0,
    "nuevo_saldo": 700.0
  }
}
```

---

## Consideraciones de Diseño

1. **Inmutabilidad del historial**: Se usa `.copy()` y `deepcopy()` para evitar referencias externas al historial.
2. **Manejo de errores**: Todas las operaciones validan entradas y lanzan `ValueError` con mensajes claros.
3. **Actualización en tiempo real**: El portafolio se calcula dinámicamente usando precios actuales.
4. **Símbolos normalizados**: Se espera que los símbolos se pasen como strings, pero no se fuerza mayúsculas (la implementación interna usa los símbolos tal cual se pasan).
5. **Precisión**: Se usan `float` para todas las cantidades monetarias (adaptado a simulación; en producción usar `Decimal`).