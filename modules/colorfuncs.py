"""Color Funcs module to handle color management.
SEE ALSO: 'colorsys' module in Python standard library.
"""
from random import randint, random
from colorsys import *

from misc import *

def hex_to_rgb(hex: str) -> str | tuple:
    """Transforma facilmente un numero hexadecimal a rgb"""
    if not hex.startswith("#") or len(hex[1:]) != 6:
        return cFormatter("El parametro | hex | debe ser un numero hexadecimal con 6 digitos.", color="red")
    else:
        rgb = []
        for i in (0, 2, 4):
            decimal = int(hex[i:i+2], 16)
            rgb.append(decimal)
        return tuple(rgb)

def rgb_to_hex(rgb):
    ...

def randomHex() -> str:
    """Devuelve un numero hexadecimal aleatorio"""
    random_number = randint(0,16777215)
    hex_number = str(hex(random_number))
    hex_number ='#'+ hex_number[2:]
    return cFormatter(f"El numero hexadecimal generado es: {Fore.LIGHTWHITE_EX}{hex_number}", color="green")

def randomRgb() -> str:
    """Devuelve un numero rgb aleatorio"""
    r = randint(0,255)
    g = randint(0,255)
    b = randint(0,255)
    return cFormatter(f"El numero rgb generado es: {Fore.LIGHTWHITE_EX}({r},{g},{b})", color="green")

def random_palette(n: int) -> str:
    """Devuelve una paleta de colores aleatoria.
    
    ## Parametros:
    
       ``n (int)``: Numero de colores que contedrá la paleta de colores generada."""
    ...

if __name__ == "__main__":
    print(randomHex())
    print(randomRgb())
    print(hex_to_rgb(randomHex()))