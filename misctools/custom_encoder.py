import base64
from enum import Enum
from dataclasses import dataclass

"""
Control de flujo | Explicacion del metodo propuesto

Remarco los siguientes puntos o fases:

1. Modelos de codificacion:
   Pueden haber mucas formas de poder codificar los archivos.
   Se puede codificar a base de numeros (correlaciones o cojuntos de numeros que son iguales a x palabra),
   a base de numeros y letras (metodo alfanumerico), a base de letras (metodo de caracteres) o a base de caracteres ascii (signos y caracteres especiales)
   Por lo tanto, se plantean los siguientes metodos:
    
    - Metodo numerico: Cada letra tiene un conjuto o correlacion UNICA de numeros. Es decir, cada letra tendrá un conjunto unico de numeros pero repetible de forma
    inversa para otra palabra.
    >>> "A" = [1, 2, 3, 4]
    >>> "B" = [2, 3, 4, 5]
"""


class Errors(Exception):
    "Base exception class for all encoder exceptions."
    
    def __init__(self): ...


class constants:
    _LETTERS = list("abcdefghijklmnñopqrstuvwxyz")
    
    def __init__(self) -> None:
        self._make_constants()

    def _make_constants(self) -> dict:
        self.constsMapping = {}
        ...