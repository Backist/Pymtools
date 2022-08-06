"""Color Funcs module to handle color management.
SEE ALSO: 'colorsys' module in Python standard library.
"""
from random import randint, random
from colorsys import *

from misc import *

def hex_to_rgb(hexc: str) -> str | tuple:
    """Transforma facilmente un numero hexadecimal a rgb"""
    if not hexc[0] == "#":
        return cFormatter("El parametro | hex | debe ser un numero hexadecimal con 6 digitos.", color="red")
    else:
        ...

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
    rgb_color = (r,g,b)
    return cFormatter(f"El numero rgb generado es: {Fore.LIGHTWHITE_EX}({r},{g},{b})", color="green")

def randomHsl() -> str:
    """Devuelve un numero hsl aleatorio.
    Este codigo de colores es mas utilizado por en la fotografia.
    """
    #h -> 0-360 | Hue
    #s -> 0-100 | Saturation
    #l -> 0-100 | Lightness
    h = randint(0,360)
    s = randint(0,100)
    l = randint(0,100)
    hsl_color = (h,s,l)
    return cFormatter(f"El numero hsl generado es: {Fore.LIGHTWHITE_EX}{hsl_color}", color="green")

def randomHsv() -> str:
    """Devuelve un numero hsv aleatorio"""
    #h -> 0-360 | Hue
    #s -> 0-100 | Saturation
    #v -> 0-100 | Value
    h = randint(0,360)
    s = randint(0,100)
    v = randint(0,100)
    hsv_color = (h,s,v)
    return cFormatter(f"El numero hsv generado es: {Fore.LIGHTWHITE_EX}({h},{s},{v})", color="green")


if __name__ == "__main__":
    e = randomHex()
    print(e)
    print(randomRgb())
    print(hex_to_rgb(randomHex()))