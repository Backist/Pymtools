from pathlib import Path
from random import choice
from logging import warning #, info, critical, error
from os.path import getsize
from turtle import back
from typing import TypeVar #, Iterable[list[str]]
from mmap import mmap

from colorama import Fore, Back, Style
# from colorama.ansi import AnsiFore, AnsiBack, AnsiStyle


__all__ = ["cFormatter", "validatePath", "readlines"]


def cFormatter(
    string: str,
    color: str, 
    style: str = None, 
    background: str = None,
    random: bool = False, 
    iter_colors: list[Fore] = [],
    forline: bool = False
    #textFile: Path = None
) -> str:
    """
    Formateador de texto en terminal.
    Valido con cadenas de texto, listas de texto y docstring.
    
    # Parametros:

    - ``string (str)``: String, docstring o archivo de texto que se va a formatear.\n
        *Nota: `Si se pasa un archivo, se lee el archivo y se devuelve el archivo con el texto formateado. IMPORTANTE: NO SE PUEDE ITERAR COLORES. `
    - ``color (str)``: Color del texto.
    - ``style (str)``: Estilo del texto.
    - ``background (str)``: Color de fondo *highlighter | subrayador.
    - ``random (bool) = False``: Elegir un patron aleatorio (selecciona un color, style y background aleatorio).
    - ``iter_colors (list) = []``: Lista de colores para iterar sobre el texto.
    - ``forline (bool) = False``: Si se debe iterar cada color de la lista por cada linea de texto.
    - *``textFile (Path) = None``: Opcionalmente se puede pasar un archivo de texto para formatearlo. Aun en pruebas

    ## Parametros validos:

      - Colores: ``BLACK | BLUE | CYAN | GREEN | LIGHTBLACK_EX |LIGHTBLUE_EX | LIGHTCYAN_EX | LIGHTGREEN_EX | LIGHTMAGENTA_EX | 
      LIGHTRED_EX | LIGHTWHITE_EX | LIGHTYELLOW_EX | MAGENTA | RED | WHITE | YELLOW``
    """
    # init(autoreset= autoreset)

    colors = vars(Fore)
    styles = vars(Style)
    backgrounds = vars(Back)
    color = color.upper()
    style = style.upper() if style is not None else None
    background = background.upper() if background is not None else None
 
    if not color in colors.keys():
        suggestions = [ck for ck in colors.keys() if (ck[0] and ck[-1] == color[0] and color[-1]) or 
        (ck[5:][:1] == color[5:][:1] if color.startswith("LIGHT") else ck[:3] == color[:3])
        ]
        return f"""{Fore.RED}| {color} | no es un color valido{Fore.RESET}.
        {Fore.BLUE}Quisiste decir {[s for s in suggestions]}?.{Fore.RESET}
        Colores validos: {Fore.LIGHTYELLOW_EX}{[c for c in colors if c != 'RESET']}{Fore.RESET}
        """
    elif background is not None and not background in backgrounds.keys():
        suggestions = [bk for bk in backgrounds.keys() if (bk[0] and bk[-1] == color[0] and color[-1]) or 
        (bk[5:][:1] == color[5:][:1] if color.startswith("LIGHT") else bk[:3] == color[:3])
        ]
        return f"""{Fore.RED}| {style} | no es un estilo valido.{Fore.RESET}
        {Fore.BLUE}Quisiste decir {[s for s in suggestions]}?.{Fore.RESET}
        Estilos validos: {Fore.LIGHTYELLOW_EX}{[s for s in styles if s != 'RESET_ALL']}{Fore.RESET}
        """
    elif style is not None and not style in styles.keys():
        suggestions = [sk for sk in styles.keys() if (sk[0] and sk[-1] == color[0] and color[-1]) or 
        (sk[5:][:1] == color[5:][:1] if color.startswith("LIGHT") else sk[:3] == color[:3])
        ]
        return f"""{Fore.RED}| {background} | no es un subrayador/background valido.{Fore.RESET}
        {Fore.BLUE}Quisiste decir {[s for s in suggestions]}?.{Fore.RESET}
        Backgrounds validos: {Fore.LIGHTYELLOW_EX}{[b for b in backgrounds if b != 'RESET']}{Fore.RESET}
        """
    else:
        if iter_colors:
            if len(iter_colors) == 0 or [x for x in iter_colors if x not in colors.keys()]:
                return TypeError(f"{Fore.RED}No se ha definido una lista de colores con los que iterar o algun color no es valido{Fore.RESET}.")
            else:
                if forline:
                    lines = []
                    for line in string.split("\n"):
                        lines.append(f"{colors[choice(iter_colors)]}{line}{Fore.RESET}")
                    return "\n".join(lines)
                else: 
                    letters = []
                    for chars in string:
                        letters.append(f"{choice(iter_colors)}{chars}{Fore.RESET}")
                    return "".join(letters)
        elif random:
            #* choice tambien puede elegir RESET (Que se ignora y actua como si no eligiera nada)
            rcolor = choice([cc for cc in colors.values()])
            rstyle = choice([sc for sc in styles.values()])
            rback = choice([bc for bc in backgrounds.values()])
            return f"{rcolor+rstyle+rback}{string}{Style.RESET_ALL}{Fore.RESET}{Back.RESET}"
        elif color:
            if background:
                return f"{colors[color]}{backgrounds[background]}{string}{Fore.RESET}{Back.RESET}"
            elif style:
                return f"{colors[color]}{styles[style]}{string}{Fore.RESET}{Style.RESET_ALL}"
            else:
                return f"{colors[color]}{string}{Fore.RESET}"
        else:
            return f"{Fore.LIGHTYELLOW_EX}Ha habido un error a la hora de formatear el texto{Fore.RESET}"


def validatePath(path: Path | str) -> bool:
    """Retorna un booleano dependiendo de si el Path o el Path de la string existe o es un archivo"""
    if isinstance(path, str):
        fpath = Path(path)
        if not fpath.exists() or not fpath.is_file():
            return False
        else:
            return True
    elif isinstance(path, Path) and not path.exists() or not path.is_file():
        return False
    else:
        return True


def readlines(StrOrPath: Path | str) -> list[int]:
    """Lee las lineas de un archivo y devuelve el numero de lineas.\n
    ``list[0]`` -> Total lines\n
    ``list[1]`` -> Total lines without White lines\n
    ``list[2]`` -> White lines
    """
    if validatePath(StrOrPath):
        with open(StrOrPath if isinstance(StrOrPath, Path) else Path(StrOrPath), "r+b") as log:
            if getsize(log.name) == 0:
                return warning("El archivo esta vacio")
            else:
                pass
            mm = mmap.mmap(log.fileno(), 0, access=mmap.ACCESS_READ)
            total_lines = 0
            white_lines = 0

            for line in iter(mm.readline, b""):     #* b"" para leer en binario. El salto de linea == '\r\n'
                if line == b"\r\n":         
                    white_lines += 1
                else:
                    total_lines += 1
            log.close()                    
        return [total_lines+white_lines, total_lines, white_lines]
    else:
        return validatePath(StrOrPath)


if __name__ == "__main__":

    er = r"""Esto es una pequeña prueba.
    Cabezera 1:
        - Ejemplo 1
        - Ejemplo 2
        - Ejemplo 3
        - Ejemplo 4
        Sub-cabezera 2:
            - Ejemplo 1
            - Ejemplo 2
    Baqueto
    """
    e = cFormatter(
        er,
        color="RED", 
        iter_colors= ["BLUE", "GREEN", "YELLOW", "RED", "BLUE", "GREEN", "YELLOW", "RED"],
        forline= True
    )
    print(e)
