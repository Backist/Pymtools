"""Color Funcs module to handle color management.
SEE ALSO: 'colorsys' module in Python standard library.
"""
from random import randint, random
from colorsys import *
from urllib.request import urlretrieve
import math

from extcolors import extract_from_image
from PIL import Image, ImageDraw
from matplotlib import gridspec
import matplotlib.pyplot as plt
import PIL

from misc import *

def hex_to_rgb(hex: str) -> str | tuple:
    """Transforma facilmente un numero hexadecimal a rgb"""
    if not hex.startswith("#") or len(hex[0+1:]) != 6:
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


#TODO: /////////////////////////////////////////  IMAGE COLOR STUDY   /////////////////////////////////////////////
#TODO: In process / a lot of errors

def study_image(image_path):
    print(cFormatter("Estudiando la imagen via HTTPS...", color="green"))
    img = _fetch_img(image_path)
    colors = _sch_extract_colors(img)
    color_palette = _render_color_platte(colors)
    _overlay_palette(img, color_palette)
    print(cFormatter("Estudio finalizado.Se ha creado una pestaña con el estudio de la imagen correctamente", color="green"))

def _fetch_img(image_path):
    print(cFormatter("Leyendo la imagen y creando un espacio temporal en su disco...", color="green"))
    try:
        urlretrieve(image_path, "image")
    except Exception as e:
        print(cFormatter(f"Error al leer la imagen: {e}", color="red"))
        exit()
    finally:
        img = PIL.Image.open("image")
    return img

def _sch_extract_colors(img):
    print(cFormatter("Extrayendo el patron de colores de la imagen...", color="green"))
    tolerance = 32
    limit = 24
    colors, pixel_count = extract_from_image(img, tolerance, limit)
    return colors

def _render_color_platte(colors):
    print(cFormatter("Renderizando la paleta y creando una capa...", color="green"))
    size = 100
    columns = 6
    width = int(min(len(colors), columns) * size)
    height = int((math.floor(len(colors) / columns) + 1) * size)
    result = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    canvas = ImageDraw.Draw(result)
    for idx, color in enumerate(colors):
        x = int((idx % columns) * size)
        y = int(math.floor(idx / columns) * size)
        canvas.rectangle([(x, y), (x + size - 1, y + size - 1)], fill=color[0])
    return result

def _overlay_palette(img, color_palette):
    print(cFormatter("Creando una pestaña con el estudio de la imagen y la paleta renderizada...", color="green"))
    nrow = 2
    ncol = 1
    f = plt.figure(figsize=(20,30), facecolor='None', edgecolor='k', dpi=55, num=None)   # Crea una figura de 20x30 pixeles para la paleta de colores
    gs = gridspec.GridSpec(nrow, ncol, wspace=0.0, hspace=0.0)                           # Crea un grid de 2x1, con un espacio de 0 entre filas y columnas
    f.add_subplot(2, 1, 1)
    plt.imshow(img, interpolation='nearest')                                             # Muestra la imagen original en la primera fila del grid
    plt.axis('off')                                                                      # Deshabilita los ejes de la imagen
    f.add_subplot(1, 2, 2)
    plt.imshow(color_palette, interpolation='nearest')
    plt.axis('off')
    plt.subplots_adjust(wspace=0, hspace=0, bottom=0)
    plt.show(block=True)

if __name__ == "__main__":
    print(randomHex())
    print(randomRgb())
    print(hex_to_rgb(randomHex()))
    image_url = 'https://astelus.com/wp-content/viajes/Lago-Moraine-Parque-Nacional-Banff-Alberta-Canada.jpg'
    study_image(image_url)