```markdown
# Diseño detallado del módulo cuentas.py

Este diseño describe una implementación Python para un sistema simple de gestión de cuentas para una plataforma de simulación de trading. Todo se organizará dentro de un solo módulo llamado `cuentas.py`.

---

## Clase principal

### Cuenta

Representa una cuenta de usuario que permite gestionar depósitos, retiros, compras y ventas de acciones, y consultar estado y transacciones.

**Atributos internos (privados):**

- `_saldo_efectivo: float`  
  Saldo disponible en efectivo (dinero no invertido).

- `_deposito_inicial: float`  
  Monto total depositado inicialmente (acumulado de depósitos).

- `_tenencias: Dict[str, int]`  
  Diccionario que mapea símbolo de acción (ej. "AAPL") a la cantidad de acciones poseídas.

- `_transacciones: List[Dict]`  
  Lista de transacciones realizadas. Cada transacción es un diccionario con campos:  
  - `tipo`: "deposito", "retiro", "compra", "venta"  
  - `simbolo`: (opcional) símbolo de acción  
  - `cantidad`: (opcional) cantidad de acciones o monto dinero  
  - `precio_unitario`: (opcional) precio por acción en transacciones de compra/venta  
  - `fecha`: timestamp o string fecha (puede ser asignado en el momento de la transacción)

---

## Funciones externas en el módulo

```python
def get_share_price(symbol: str) -> float:
    """
    Función simulada para obtener el precio actual de una acción.
    Implementación de prueba incluye precios fijos para:
    - AAPL: 150.0
    - TSLA: 700.0
    - GOOGL: 2800.0

    Parámetros:
    - symbol: str, síbolo de la acción

    Retorna:
    - float: precio unitario actual de la acción

    Lanza excepción si símbolo no reconocido.
    """
```

---

## Métodos públicos de la clase Cuenta

```python
class Cuenta:

    def __init__(self):
        """
        Inicializa una cuenta vacía con saldo cero y sin tenencias.
        """
    
    def depositar(self, monto: float) -> None:
        """
        Deposita fondos en la cuenta, incrementando saldo efectivo y depósito inicial.
        Parámetros: 
            - monto: float, monto positivo a depositar
        Lanza excepción si monto <= 0.
        Registra la transacción.
        """

    def retirar(self, monto: float) -> None:
        """
        Retira fondos del saldo efectivo.
        Parámetros:
            - monto: float, monto positivo a retirar
        Lanza excepción si monto <= 0 o si el retiro dejaría saldo negativo.
        Registra la transacción.
        """

    def comprar_acciones(self, simbolo: str, cantidad: int) -> None:
        """
        Registra la compra de acciones.
        Parámetros:
            - simbolo: str, símbolo de la acción (ej. "AAPL")
            - cantidad: int, cantidad de acciones a comprar (> 0)
        Valida que el usuario tiene saldo efectivo suficiente para pagar la compra.
        Actualiza tenencias y saldo efectivo.
        Registra la transacción (incluye precio unitario actual).
        Lanza excepción en caso de fondos insuficientes o cantidad inválida.
        """

    def vender_acciones(self, simbolo: str, cantidad: int) -> None:
        """
        Registra la venta de acciones.
        Parámetros:
            - simbolo: str, símbolo de la acción
            - cantidad: int, cantidad de acciones a vender (> 0)
        Valida que el usuario posee suficientes acciones.
        Aumenta el saldo efectivo según precio unitario actual * cantidad.
        Actualiza tenencias y saldo.
        Registra la transacción (incluye precio unitario actual).
        Lanza excepción si la cantidad inválida o acciones insuficientes.
        """

    def obtener_tenencias(self) -> Dict[str, int]:
        """
        Retorna un diccionario con las tenencias actuales (símbolo -> cantidad).
        """

    def valor_portafolio(self) -> float:
        """
        Calcula y retorna el valor total del portafolio actual:
        saldo efectivo + suma (cantidad acciones * precio actual).
        """

    def ganancias_perdidas(self) -> float:
        """
        Calcula y retorna la ganancia o pérdida neta en relación al depósito total:
        (valor_portafolio - deposito_inicial)
        Puede ser positivo o negativo.
        """

    def listar_transacciones(self) -> List[Dict]:
        """
        Retorna la lista completa de transacciones realizadas en orden cronológico.
        Cada transacción incluye tipo, símbolo (si aplica), cantidad, precio unitario (si aplica), y fecha.
        """

```

---

## Consideraciones adicionales

- Se usará manejo básico de excepciones para invalidar operaciones no permitidas (fondos insuficientes, cantidades <=0, símbolos inválidos).
- Las fechas en transacciones serán definidas en el momento de la operación, usando datetime estándar.
- El sistema solo maneja tres acciones con precio fijo para pruebas, pero la estructura permite ampliar `get_share_price`.
- Todas las unidades monetarias serán float para permitir centavos.
- El estado interno es privado para evitar manipulación externa directa.

---

## Resumen

| Clase     | Método                 | Función principal                                            |
|-----------|------------------------|-------------------------------------------------------------|
| Cuenta    | `__init__()`           | Crear cuenta vacía                                           |
| Cuenta    | `depositar(monto)`     | Depositar efectivo en la cuenta                              |
| Cuenta    | `retirar(monto)`       | Retirar efectivo, sin saldo negativo                         |
| Cuenta    | `comprar_acciones(s, c)`| Comprar acciones si hay fondos suficientes                   |
| Cuenta    | `vender_acciones(s, c)`| Vender acciones si se poseen suficientes                     |
| Cuenta    | `obtener_tenencias()`  | Devolver las tenencias actuales                              |
| Cuenta    | `valor_portafolio()`   | Calcular valor total actual (efectivo + acciones)            |
| Cuenta    | `ganancias_perdidas()` | Calcular ganancias/perdidas respecto al depósito inicial    |
| Cuenta    | `listar_transacciones()` | Listar todas las transacciones realizadas                    |
| Módulo    | `get_share_price(symbol)`| Retorna precio actual de la acción (prueba con valores fijos)|

Este diseño es completamente autónomo en un solo módulo, se facilitará su implementación, pruebas unitarias y ampliaciones futuras.

```