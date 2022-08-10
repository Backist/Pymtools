"""Color Funcs module to handle color management.
SEE ALSO: 'colorsys' module in Python standard library.
"""
from random import randint as _randint
from colorama import Fore as _Fore

from matplotlib.colors import to_hex, to_rgba, to_rgb

from misc import cFormatter

__all__ = [
    "hex2rgb",
    "rgb2hex",
    "rgb2hsv",
    "randomHex",
    "randomRgb",
    "randomHsl",
    "randomHsv"
]

def hex2rgb(hexc: str) -> str | tuple:
    """Transforma facilmente un numero hexadecimal a rgb con el metodo ``colorsys.to_rgb()``"""
    if not hexc.startswith('#') or len(hexc) != 6:
        return cFormatter("El parametro | hex | debe ser un numero hexadecimal con 6 digitos.", color="red")
    return to_rgb(hexc)

def rgb2hex(rgb):
    try:
        return to_hex(rgb)
    except Exception as e:
        return cFormatter(f"Error al formatear el numero rgb a hexadecimal.\n{_Fore.LIGHTYELLOW_EX}Callback: {e}", color="red")

def rgb2hsv(rgb: tuple[float, float, float], prettyPrint: bool = False) -> str:
    #rgb to hsv convertion formula:
    #https://www.researchgate.net/figure/relation-between-RGB-and-HSV-And-the-reveres-wise-conversion-HSV-color-space-to-RGB_fig5_315744580
    
    if not isinstance(rgb ,tuple) or len(rgb) != 3:
        return cFormatter("El parametro | rgb | debe ser una tupla con 3 valores numéricos.", color="red")
    elif not all(isinstance(x, (int, float)) and 0<=x<=255 for x in rgb):
        return cFormatter("Los valores de la tupla deben ser numéricos y no superiores a 255. (RGB codex)", color="red")
    try:
        r,g,b = float(rgb[0]), float(rgb[1]), float(rgb[2])
    except Exception as e:
        return cFormatter(f"Error al formatear el numero rgb a hsv.\n{_Fore.LIGHTYELLOW_EX}Callback: {e}", color="red")

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
        return cFormatter(f"El numero hsv generado del rgb es: {_Fore.LIGHTWHITE_EX}{hsv_color}", color="green")
    return hsv_color

def randomHex(prettyPrint: bool = False) -> str:
    """Devuelve un numero hexadecimal aleatorio.\n
    Si ``prettyPrint`` es True, devuelve un string coloreado con el numero hexadecimal creado.
    """
    random_number = _randint(0,16777215)
    hex_number = str(hex(random_number))
    hex_number ='#'+ hex_number[2:]
    if prettyPrint:
        return cFormatter(f"El numero hexadecimal generado es: {_Fore.LIGHTWHITE_EX}{hex_number}", color="green")
    return hex_number

def randomRgb(prettyPrint: bool = False, toRgba: bool = False) -> str:
    """Devuelve un numero rgb aleatorio\n
    Si ``prettyPrint`` es True, devuelve un string coloreado con el numero hexadecimal creado.
    Si ``toRgba`` es True, devuelve una tupla con el numero rgba creado.
    """
    r = _randint(0,255)
    g = _randint(0,255)
    b = _randint(0,255)
    rgb_color = r,g,b
    if prettyPrint:
        return cFormatter(f"El numero rgb generado es: {_Fore.LIGHTWHITE_EX}{rgb_color if not toRgba else to_rgba(rgb_color)}", color="green")
    return rgb_color if not toRgba else to_rgba(rgb_color)

def randomHsl(prettyPrint: bool = False) -> str:
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
        return cFormatter(f"El numero hsl generado es: {_Fore.LIGHTWHITE_EX}{hsl_color}", color="green")
    return hsl_color

def randomHsv(prettyPrint: bool = False) -> str:
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
        return cFormatter(f"El numero hsv generado es: {_Fore.LIGHTWHITE_EX}{hsv_color}", color="green")
    return hsv_color


if __name__ == "__main__":
    e = randomHex()
    f = randomRgb(True)
    print(f)
    d = rgb2hsv((255,255,255), True)
    print(d)    