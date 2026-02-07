#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from teamcoders.crew import Teamcoders

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

requirements="""
Un sistema simple de gestión de cuentas para una plataforma de simulación de trading.
El sistema debe permitir a los usuarios crear una cuenta, depositar y retirar fondos.
El sistema debe permitir a los usuarios registrar que han comprado o vendido acciones,
indicando una cantidad.
El sistema debe calcular el valor total del portafolio del usuario y las ganancias
o pérdidas respecto al depósito inicial.
El sistema debe poder informar las tenencias del usuario en cualquier momento.
El sistema debe poder informar las ganancias o pérdidas del usuario en cualquier momento.
El sistema debe poder listar las transacciones que el usuario ha realizado a lo largo
del tiempo.
El sistema debe evitar que el usuario retire fondos que lo dejen con un saldo negativo,
compre más acciones de las que puede pagar o venda acciones que no posee.
El sistema tiene acceso a una función get_share_pryce(symbol) que devuelve el precio
actual de una acción, e incluye una implementación de prueba que devuelve precios
fijos para AAPL, TSLA y GOOGL.
"""
module_name="cuentas.py"
class_name="Cuenta"

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'requirements': requirements,
        'module_name': module_name,
        'class_name': class_name,
    }

    try:
        Teamcoders().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

