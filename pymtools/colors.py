"""Color Funcs module to handle color management.
SEE ALSO: ``colorama & colorsys`` to more advanced color functions.
"""
from random import randint as _randint

from matplotlib.colors import to_hex as _to_hex, to_rgb as _to_rgb #, _to_rgba
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mplc

# Podemos importar _Fore del modulo misc en lugar de tener que importarlo de la librería de nuevo
from .misc import cFormatter as _cFormatter, _Fore


__all__ = [
    "hex2rgb",
    "rgb2hex",
    "rgb2hsv",
                "randomHex",
                "randomRgb",
                "randomHsl",
                "randomHsv"
]


def _check_valid_color(c: str | tuple[int, int, int], _type: str):
    ...
        

def hex2rgb(hexc: str) -> str | tuple:
    """Transforma facilmente un numero hexadecimal a rgb con el metodo ``matplotlib.colors.to_rgb()``"""
    if not hexc.startswith('#') or len(hexc) != 6:
        raise TypeError(f"{_Fore.RED}El parametro | hex | debe ser un numero hexadecimal con 6 digitos.{_Fore.RESET}")
    return _to_rgb(hexc)


def rgb2hex(rgb):
    try:
        return _to_hex(rgb)
    except Exception as e:
        raise ValueError(f"{_Fore.RED}Error al formatear el numero rgb a hexadecimal.\n{_Fore.LIGHTYELLOW_EX}Callback: {e}{_Fore.RESET}")


def rgb2hsv(rgb: tuple[float, float, float], prettyPrint: bool = False) -> str:
    #rgb to hsv convertion formula:
    #https://www.researchgate.net/figure/relation-between-RGB-and-HSV-And-the-reveres-wise-conversion-HSV-color-space-to-RGB_fig5_315744580
    
    if not isinstance(rgb ,tuple) or len(rgb) != 3:
        raise TypeError(f"{_Fore.RED}El parametro | rgb | debe ser una tupla con 3 valores numéricos.{_Fore.RESET}")
    elif not all(isinstance(x, (int, float)) and 0<=x<=255 for x in rgb):
        raise TypeError(f"{_Fore.RED}Los valores de la tupla deben ser numéricos y no superiores a 255. (RGB codex){_Fore.RESET}")
    try:
        r,g,b = float(rgb[0]), float(rgb[1]), float(rgb[2])
    except Exception as e:
        raise Exception(f"{_Fore.RED}Error al formatear el numero rgb a hsv.\n{_Fore.LIGHTYELLOW_EX}Callback: {e}{_Fore.RED}")

    rc,gc,bc = r/255, g/255, b/255
    cmax = max(rc, gc, bc)
    cmin = min(rc, gc, bc)
    delta = cmax - cmin
    if delta == 0:
        h = 0
    elif cmax == rc:
        h = 60 * (((gc - bc) / delta) % 6)
    elif cmax == gc:
        h = 60 * ((bc - rc) / delta + 2)
    elif cmax == bc:
        h = 60 * ((rc - gc) / delta + 4)
    if cmax == 0:
        s = 0
    else:
        s = delta / cmax
    v = cmax
    hsv_color = round(h),round(s*100),round(v*100)
    if prettyPrint:
        return _cFormatter(f"El numero hsv generado del rgb es: {_Fore.LIGHTWHITE_EX}{hsv_color}", color="green", style= "bright")
    return hsv_color


def randomHex(prettyPrint: bool = False) -> str:
    """Devuelve un numero hexadecimal aleatorio.\n
    Si ``prettyPrint`` es True, devuelve un string coloreado con el numero hexadecimal creado.
    """
    # random_number = _randint(0,16777215)
    # hex_number ='#'+ str(hex(random_number))[2:]
    r, g, b = _randint(0,255), _randint(0,255), _randint(0,255)
    hex_number = r,g,b
    if prettyPrint:
        return _cFormatter(f"El numero hexadecimal generado es: {_Fore.LIGHTWHITE_EX}{hex_number}", color="green", style= "bright")
    return "#{:02x}{:02x}{:02x}".format(r,g,b)


def randomRgb(prettyPrint: bool = False, toRgba: bool = False) -> str | tuple[int ,int ,int]:
    """Devuelve un numero rgb aleatorio\n
    Si ``prettyPrint`` es True, devuelve un string coloreado con el numero hexadecimal creado.

    - En versiones futuras se añadirá el parametro ``'rgba'``.
    """
    r = _randint(0,255)
    g = _randint(0,255)
    b = _randint(0,255)
    rgb_color = r,g,b
    if prettyPrint:
        return _cFormatter(f"El numero rgb generado es: {_Fore.LIGHTWHITE_EX}{rgb_color}", color="green", style= "bright")
    return rgb_color


def randomHsl(prettyPrint: bool = False) -> str | tuple[int ,int ,int]:
    """Devuelve un numero hsl aleatorio.
    Este codigo de colores es mas utilizado en el campo fotografia.\n
    Si ``prettyPrint`` es True, devuelve un string coloreado con el numero hexadecimal creado.
    """
    #h -> 0-360 | Hue
    #s -> 0-100 | Saturation
    #l -> 0-100 | Lightness
    h = _randint(0,360)
    s = _randint(0,100)
    l = _randint(0,100)
    hsl_color = h,s,l
    if prettyPrint:
        return _cFormatter(f"El numero hsl generado es: {_Fore.LIGHTWHITE_EX}{hsl_color}", color="green", style= "bright")
    return hsl_color


def randomHsv(prettyPrint: bool = False) -> str | tuple[int ,int ,int]:
    """Devuelve un numero hsv aleatorio
    Este codigo de colores es mas utilizado en el campo fotografia.\n
    Si ``prettyPrint`` es True, devuelve un string coloreado con el numero hexadecimal creado.
    """
    #h -> 0-360 | Hue
    #s -> 0-100 | Saturation
    #v -> 0-100 | Value
    h = _randint(0,360)
    s = _randint(0,100)
    v = _randint(0,100)
    hsv_color = h,s,v
    if prettyPrint:
        return _cFormatter(f"El numero hsv generado es: {_Fore.LIGHTWHITE_EX}{hsv_color}", color="green", style= "bright")
    return hsv_color


def randomPalette(size: int = 8, only_hex: bool = False):
    palette_array = []
    if not isinstance(size, int):
        raise TypeError("El parametro debe ser un numero indicando el tamaño de la paleta que se va a generar.")
    for i in range(size):
        palette_array.append(randomHex())
    return palette_array


def palette_viewer(colors: list[str]):
    data = mplc.to_rgba_array(colors)
    plt.imshow(np.array(data).reshape((20, 50, 4)))  #! Valores del reshape originales (20, 50, 4)
    plt.grid(False)
    plt.show()


print(randomPalette(20))
palette_viewer(randomPalette(1000))
    

    