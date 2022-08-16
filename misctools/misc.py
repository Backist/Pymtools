"""
Miscellaneous Tools module.

This module contains various tools that can be used in some projects to improve the code.
"""
from collections import namedtuple as _namedtuple, OrderedDict as _OrderedDict
from numbers import Number as _Number
from pathlib import Path as _Path
from pprint import pformat as _pformat
from random import choice as _choice# , randbytes as _randbytes, random as _random
from os.path import getsize as _getsize
from datetime import datetime as _datetime
from typing import TypeAlias as _TypeAlias, Optional as _Optional, TypeVar
from mmap import mmap as _mmap, ACCESS_READ as _ACCESS_READ #, ACCESS_WRITE
from threading import Thread as _Thread
from json import dumps as _dumps
import time as _t

from colorama import Fore as _Fore, Back as _Back, Style as _Style

__all__: list[str] = [
    "cFormatter",
    "readlines",
    "countlines",
    "validatePath", 
    "morphTo",
    "is_email", 
    "is_phone",
    "ordered",
    "joinmany",
    "sensiblePrint",
    "get_key", 
    "ftime", 
    "createTimer"
]

anyCallable: _TypeAlias = type
Any = object


def cFormatter(
    string: str,
    color: str, 
    style: _Optional[str] = None, 
    background: _Optional[str] = None,
    random: bool = False, 
    iter_colors: list[str] = [],
    forline: bool = False
    #textFile: Path = None
) -> str:
    """
    Formateador de texto en terminal.
    Valido con cadenas de texto, listas de texto y docstring.
    
    # Parametros:

    - ``string (str)``: String, docstring o archivo de texto que se va a formatear.
            - *NOTA: `Si se pasa un archivo, se lee el archivo y se devuelve el archivo con el texto formateado. IMPORTANTE: NO SE PUEDE ITERAR COLORES. `
    - ``color (str)``: Color del texto.
    - ``style (str)``: Estilo del texto.
    - ``background (str)``: Color de fondo *highlighter | subrayador.
    - ``random (bool) = False``: Elegir un patron aleatorio (selecciona un color, style y background aleatorio).
    - ``iter_colors (list) = []``: Lista de colores para iterar sobre el texto.\n
            - *NOTA: Si se pasa una lista de colores, se itera ALEATORIAMENTE sobre el texto. Si se desea iterar cada color por cada linea, ponga el 'forline' parametro.
    - ``forline (bool) = False``: Si se debe iterar cada color de la lista por cada linea de texto.
    - *``textFile (Path) = None``: Opcionalmente se puede pasar un archivo de texto para formatearlo. Aun en pruebas

    ## Parametros validos:

      - Colores & Backgrouds: ``BLACK | BLUE | CYAN | GREEN | LIGHTBLACK_EX |LIGHTBLUE_EX | LIGHTCYAN_EX | LIGHTGREEN_EX | LIGHTMAGENTA_EX |``
      ``LIGHTRED_EX | LIGHTWHITE_EX | LIGHTYELLOW_EX | MAGENTA | RED | WHITE | YELLOW``
      
      - Estilos: ``BRIGHT | DIM | NORMAL`
            - *NOTA: Ambos parametros ``color`` y ``background`` aceptan los mismo colores 
    """
    # init(autoreset= autoreset)

    colors = vars(_Fore)
    styles = vars(_Style)
    backgrounds = vars(_Back)
    try:
        color = color.upper()
        style = style.upper() if style is not None else None
        background = background.upper() if background is not None else None
        iter_colors = [color.upper() for color in iter_colors] if len(iter_colors) > 0 else []
    except AttributeError as a:
        return f"{_Fore.RED}Los parametros deben ser de tipo: {_Fore.YELLOW}color-> str | style-> str | background-> str.{_Fore.RESET}.\nCallback: {a}"


    if not color in colors.keys():
        suggestions = [ck for ck in colors.keys() if (ck[0] and ck[-1] == color[0] and color[-1]) or 
        (ck[5:][:1] == color[5:][:1] if color.startswith("LIGHT") else ck[:3] == color[:3]) or ck.startswith(color[0])
        ]
        return f"""{_Fore.RED}| {color} | no es un color valido.{_Fore.RESET}{_Fore.BLUE}
        Quisiste decir {[s for s in suggestions if s != "RESET"]}?{_Fore.RESET}
        Colores validos: {_Fore.LIGHTYELLOW_EX}{[c for c in colors if c != 'RESET']}{_Fore.RESET}
        """
    elif background is not None and not background in backgrounds.keys():
        suggestions = [bk for bk in backgrounds.keys() if (bk[0] and bk[-1] == background[0] and background[-1]) or 
        (bk[5:][:1] == background[5:][:1] if background.startswith("LIGHT") else bk[:3] == background[:3]) or bk.startswith(background[0])
        ]
        return f"""{_Fore.RED}| {background} | no es un background valido.{_Fore.RESET}{_Fore.BLUE}
        Quisiste decir {[s for s in suggestions if s != "RESET"]}?{_Fore.RESET}
        Backgrounds validos: {_Fore.LIGHTYELLOW_EX}{[s for s in backgrounds if s != 'RESET']}{_Fore.RESET}
        """
    elif style is not None and not style in styles.keys():
        suggestions = [sk for sk in styles.keys() if sk.startswith(style[0]) or sk.endswith(style[-1]) or [char for char in style if char in sk]]
        return f"""{_Fore.RED}| {style} | no es un estilo valido.{_Fore.RESET}{_Fore.BLUE}
        Quisiste decir {[s for s in suggestions if s != "RESET_ALL"]}?{_Fore.RESET}
        Estilos validos: {_Fore.LIGHTYELLOW_EX}{[b for b in styles if b != 'RESET_ALL']}{_Fore.RESET}
        """
    else:
        if iter_colors:
            ilegal = [x.upper() for x in iter_colors if not x.upper() in colors.keys()]
            #* si algun color no es valido, se guarda en la lista ilegal y si ilegal != 0 se devuelve un mensaje de error con el color invalido
            if len(iter_colors) == 0 or ilegal:
                return f"{_Fore.RED}No se ha definido una lista de colores con los que iterar o algun color no es valido.{_Fore.RESET}{_Fore.LIGHTCYAN_EX}\nColor Error: {[f for f in ilegal]}{_Fore.RESET}"
            else:
                if forline:
                    # #* hacemos que la lista de colores se repita tantas lineas de codigo haya (para que zip funcione)
                    # iter_colors += iter_colors * len(er.split("\n"))
                    # lines = []
                    # #* zip nos permite iterar sobre dos listas a la vez (cada elemento de una con el mismo elemento de la otra)
                    #TODO: el metodo parará cuando alguno de las dos listas se acabe
                    # for line, lc in zip(string.split("\n"), iter_colors):
                    #     lines.append(f"{colors[lc]}{line}{_Fore.RESET}")
                    iter_colors += iter_colors * len(string.split("\n"))
                    lines = list(map(lambda line, color: f"{colors[color]}{line}{_Fore.RESET}", string.split("\n"), iter_colors))
                    return "\n".join([f for f in lines])
                else: 
                    letters = []
                    for chars in string:
                        letters.append(f"{colors[_choice(iter_colors)]}{chars}{_Fore.RESET}")
                    return "".join(letters)
        elif random:
            #* choice tambien puede elegir RESET (Que se ignora y actua como si no eligiera nada)
            rcolor = _choice([cc for cc in colors.values()])
            rstyle = _choice([sc for sc in styles.values()])
            rback = _choice([bc for bc in backgrounds.values()])
            return f"{rcolor+rstyle+rback}{string}{_Style.RESET_ALL}{_Fore.RESET}{_Back.RESET}"
        elif color:
            if background:
                return f"{colors[color]}{backgrounds[background]}{string}{_Fore.RESET}{_Back.RESET}"
            elif style:
                return f"{colors[color]}{styles[style]}{string}{_Fore.RESET}{_Style.RESET_ALL}"
            else:
                return f"{colors[color]}{string}{_Fore.RESET}"
        else:
            return f"{_Fore.LIGHTYELLOW_EX}Ha habido un error a la hora de formatear el texto{_Fore.RESET}"


def readlines(pathfile: _Optional[_Path | str] = None , text: _Optional[str] = None, ToNamedTuple: bool = True) -> tuple[int, int, int] | tuple[tuple, tuple]:
    """Lee las lineas de un archivo o cadena de texto y devuelve el numero de lineas.\n
    ``tuple[0]`` -> Total lines\n
    ``tuple[1]`` -> Total lines without White lines\n
    ``tuple[2]`` -> White lines

    ## Parámetros
    - ``pathfile``: Ruta del archivo a leer.\n
    - ``text``: Cadena de texto a leer.\n
    - ``namedtuple``: Si es True devuelve una tupla nombrada con los valores de las lineas, si es False devuelve una lista con los valores de las lineas.
        - !!: Si este parametro es ``True``, podra acceder al docstring de la tupla nombrada con tuple.__doc__ () (Solo lectura)
    
    ### Importante

        - ``Los parametros estan establecidos para que ambos sean None (opcionales), pero al menos uno no debe ser None``
        - ``Si un archivo que no esta en el directorio raiz es pasado, deberá dar la ruta absoluta del archivo (no la relativa)``
        - RECOMENDACION: ``Para evitar problemas al poner la ruta, hazlo de esta forma: ``r"<root>"``, colocandola como expresion regular y evitar problemas.``
        - NOTA: ``Puede ser pasado un archivo y una cadena de texto si se desea y será devuelta una tupla con cada tupla.``

    #### Errores:

    >>> path = "c:/Users/<user>/Desktop/<file>.txt"
    >>> readlines(path)
        - Esto genera un error porque no lo reconoce como una ruta. Para ello utiliza ``//`` o coloca una ``r`` delante de la ruta.
    """

    single_tuple = _namedtuple("linesTuple", ["Total_Lines", "Without_White_Lines", "White_Lines"], defaults=[0,0,0])
    single_tuple.__doc__ = """ReadLine namedtuple\n
    DEFAULT VALUES: ``total_lines = != 0, total_lines+white_lines = 0, white_lines = 0``

    ## Elements\n
    ``total_lines`` -> Total lines of the file or text. This never will be 0.\n
    ``without_white_lines`` -> Total lines without including white lines.This field can be 0 if single string is passed.
        - NOTE: ``!Maybe this field can not work properly!``
    ``white_lines`` -> Total white lines. This field can be 0.. 
        - NOTE: !If singe line string with spaces is supplied, this field will be 0"
    """
    double_tuple = _namedtuple("linesTuple", ["pathfile_lines", "text_lines"])
    double_tuple.__doc__ = """ReadLine namedtuple\n
    This tuple of tuple returns two tuples with the lines of the file and the text.
    """

    pathfile = pathfile if pathfile is not None and isinstance(pathfile, _Path) else _Path(pathfile) if pathfile is not None else None

    if text is not None and isinstance(text, str) and pathfile is not None and validatePath(pathfile):
        return double_tuple(readlines(pathfile), readlines(None, text)) if ToNamedTuple else (readlines(pathfile), readlines(None, text))
    elif text is not None and isinstance(text, str):
        if text.count("\n") == 0:
            return single_tuple(len(text),0,0) if ToNamedTuple else (len(text),0,0)
        else:
            linelist = (
                len(text.split("\n")), 
                len([l for l in text.split("\n") if l.strip()]), 
                len([l for l in text.split("\n") if not l.strip()])
            )
            return single_tuple(*linelist) if ToNamedTuple else linelist
    elif pathfile is not None and validatePath(pathfile):
        with open(pathfile if isinstance(pathfile, _Path) else _Path(pathfile), "r+b") as file:
            if _getsize(file.name) == 0:
                return f"{_Fore.YELLOW}[FILE ERROR]: {_Fore.YELLOW}El archivo esta vacio.{_Fore.RESET}"
            else:
                pass
            mm = _mmap(file.fileno(), 0, access=_ACCESS_READ)
            total_lines = 0
            white_lines = 0

            for line in iter(mm.readline, b""):     #* b"" para leer en binario. El salto de linea == '\r\n'
                if line == b"\r\n":         
                    white_lines += 1
                total_lines += 1
            file.close()                    
        return single_tuple(total_lines, total_lines - white_lines, white_lines) if ToNamedTuple else (total_lines, total_lines - white_lines, white_lines)
    else:
        if text is None and pathfile is None:
            return f"{_Fore.RED}[PARAMS NULL ERROR]: {_Fore.YELLOW}Al menos un valor no debe ser None.{_Fore.RESET}"
        elif text is not None and not isinstance(text, str) or pathfile is not None and not isinstance(pathfile, _Path) or not isinstance(pathfile, str):
            return f"{_Fore.RED}[PARAMS TYPE ERROR]: {_Fore.YELLOW}Los valores admitidos son: `pathfile': (str | Path) y 'text': (str).{_Fore.RESET}"
        else:
            return f"{_Fore.RED}[FUNC ERROR]: Algo ha ido mal a la hora de ejecutar la funcion. Revise los parametros.{_Fore.RESET}"


def countlines(maindir: _Path | str, exclude: list = []):
    """Cuenta el numero de lineas de todos los archivos de un directorio.

    ## Parámetros
    - ``maindir``: Ruta del directorio a leer.\n
    - ``exclude``: Lista de archivos o directorios a excluir.
        - NOTA: Si no se encuentra algun archivo o directorio de la lista en el directorio, se saltará al siguiente.
        - IMPORTANTE: ``Si se quiere excluir un directorio, se deberá pasar la ruta relativa y deberá estar en el directorio actual. Verificalo con os.chdir()``

    ## Importante
        - Dentro del directorio, no se cuenta el numero de lineas de los directorios que contengan archivos.
        - Si la ruta no es absoluta devolverá una Excepción.
        - SI el directorio esta vacio devolverá una Excepcion.

    ### NOTA: El resultado del conteo de las lineas de un directorio puede no ser exacto, ya que las lineas en blanco, comentarios o espacios pueden llegar a saltarse.\n
    #### Esto es debido a que el metodo utilizado para contar las lineas no es recursivo.
    """

    if isinstance(maindir, str):
        try:
            maindir = _Path(maindir)
        except Exception as e:
            return e
    if not maindir.is_dir() or not maindir.exists():
        return f"{_Fore.RED}[PATH ERROR]: {_Fore.YELLOW}La ruta debe llevar a un directorio y debe existir.{_Fore.RESET}"
    elif not maindir.is_absolute() and not maindir.name in [p.name for p in _Path.cwd().glob("**/*")]:	
        return f"{_Fore.RED}[PATH ERROR]: {_Fore.YELLOW}La ruta debe ser absoluta si no se encuentra en el directorio actual.{_Fore.RESET}"
    else:
        total_lines = 0
        white_lines = 0
        for file in maindir.iterdir():
            if len(exclude) > 0 and file.name in exclude:
                pass
            elif file.is_dir():
                pass        #pass para pasar a la siguiente iteracion NO CONTINUE 
            elif file.is_file() and _getsize(file) != 0:
                with open(file, "r+b") as f:
                    if not f.readable() or not f.writable():
                        pass
                    mm = _mmap(f.fileno(), 0, access=_ACCESS_READ)
                    for line in iter(mm.readline, b""):
                        if line == b"\r\n":
                            white_lines += 1
                        total_lines += 1
                f.close()
        return (total_lines, total_lines - white_lines, white_lines)


def validatePath(path: _Path | str, estrict: bool = True) -> bool | None:
    """Retorna un booleano dependiendo de si el Path o el Path de la string es valido.
    ## Parámetros
    - ``path``: Ruta a validar.\n
    - ``estrict``: Si es True, se filtrará si el Path existe, o es un archivo o directorio, sino se filtrará si existe.
    """
    try:
        path = _Path(path) if isinstance(path, str) else path
    except Exception:
        return False
    return True if any([path.is_file(), path.is_dir()]) and path.exists() else False if estrict else path.exists()


def morphTo(element, to):
    """
    ### !!! [Deprecated] !!!
    #### En Python 3.10 puedes usar <class_to_transform>(<object_to_transform>) para transformar un objeto a otro. E.g: tuple(list(range(10))) or list((1,2,3,4))

    Retorna un elemento de un tipo diferente.
    ## Parámetros
    - ``element``: Elemento a convertir.\n
    - ``to``: Tipo al que se quiere convertir el elemento.

    ## ! Importante:
    - Hay una jerarquía de transformaciones:\n
        | ``dict``\n
        ||| ``set``\n
        ||| ``tuple``\n
        ||| ``list``\n
        ||||| ``bytes``\n
        ||||||| ``str``\n
        ||||||| ``int``\n
        ||||||| ``float``\n
            - Los elementos se pueden convertir entre ellos si son ``DEL MISMO ESCALON O UN ESCALON MAS BAJO`` pero hay excepciones
            - |dict| no se puede convertir a nada que no sea de su mismo escalon (porque es el unico tipo de dato que contiene datos clave-valor)
            - Hay que tener cuidado cuando intentamos transformar tipos de estructuras de datos iterables y no iterables (inmutables-mutables).
    """
    hierarchyLevels = {
        1: (
            dict.__name__
        ),
        3: (
            set.__name__, tuple.__name__, list.__name__
        ),
        5: (
            bytes.__name__,
        ),
        7: (
            str.__name__, int.__name__, float.__name__
        )
    }
    
    if not isinstance(to, type):
        return cFormatter(f"{_Fore.RED}[TYPE ERROR]: {_Fore.YELLOW}El tipo a convertir debe ser un tipo de dato (int, float, str).{_Fore.RESET}", color="red")

    _nativeType = type(element).__name__
    _transformType = to.__name__

    if _nativeType == _transformType:
        return cFormatter(f"[TYPE ERROR] Error al transformar los elementos: {_Fore.LIGHTYELLOW_EX}Los tipos son iguales.", color= "red")
    # elif _nativeType or _transformType not in [f for f in [t for t in hierarchyLevels.values()]]:
    #     return cFormatter(f"[TYPE ERROR] Error al transformar los elementos: {_Fore.LIGHTYELLOW_EX}El tipo no es compatible.", color= "red")
    else:
        if _nativeType and _transformType in hierarchyLevels[1]:
            return cFormatter(f"[TYPE ERROR] Error al transformar los elementos: {_Fore.LIGHTYELLOW_EX}No se puede transformar un diccionario a otro tipo.", color= "red")
        elif not _nativeType in hierarchyLevels[1] and _transformType in hierarchyLevels[1]:
            return cFormatter(f"[TYPE ERROR] Error al transformar los elementos: {_Fore.LIGHTYELLOW_EX}No se puede transformar un tipo no iterable a un diccionario.", color= "red")
        elif not _nativeType in hierarchyLevels[5] and not _nativeType in hierarchyLevels[1] and _transformType in hierarchyLevels[5]:
            bytes(element)
        else:
            #to reverse a list -> list[::-1]
            return to(element[::-1]) if _transformType == "set" else to(element)
        
        
def is_email(email: str):
    valids = ["gmail.com", "hotmail.com", "outlook.com", "yahoo.com", "live.com", "ymail.com", "mail.com", "protonmail.com"]

    if not email.endswith(".com") and email[email.find("@")+1:]:
        return False
    elif not email[email.find("@")+1:] in valids or not email.find("@") > 0 or not email.endswith(".com"):
        return False
    else:
        return True


def is_phone(phone: str) -> bool:
    """Verifca si un numero de telefono es valido.
    ### Importante:
    - Si se pasa el prefijo junto al numero, una Excepcion será la nzada (puesto que el parametro ``prefix`` es para ello)
    """
    phone = str(phone)
    if not phone.startswith(("0","1","2","3","4","5","6","7","8","9")):
        return False
    elif len(phone) > 19:   #max len of a phone number is 15 digits + country code (max 3 digits e.g: +234 xxxxxxxxxxx) == 19
        return False
    else:
        return True


def joinmany(obj: type, sep: str = " ") -> type | str:
    """Unifica un objeto de tipo iterable en una cadena de texto separada por el separador dado.
    
    ## Parámetros:
    - ``obj``: Objeto a unificar. El objecto debe ser iterable.\n
        - ``Si un objeto no es iterable (tuple, set, ...), se intenta juntarlo excepto que devuelva TypeError.``
        - NOTE: SI el objeto es un diccionario, se unificará de esta manera: ``"key: value  key2  value2, ..."``
    - ``sep``: Separador que se usara para unificar los elementos.
        - NOTE: El parametro ``sep`` es sensible a espacios y tabulaciones, puesto que tambien son contadas para separar los elementos. ``e.g: sep= " || "``
    """
    if isinstance(obj, dict):
        return sep.join(f"{k}:{v}" for k, v in obj.items())
    else:
        try:
            sep.join(obj)
        except TypeError:
            return obj

#! ORDERED; SortByType and SensiblePrint must have been repaired to work properly. Implement them in future versions.

def ordered(obj: type, reverse: bool = False, prettyPrint: bool = False) -> type | list | _OrderedDict:
    """Ordena un objecto de tipo iterable segun los parametros dados.
    
    ## Parámetros:

    - ``obj``: Objeto a ordenar. El objecto debe ser iterable.\n
        - ``Si un objeto no es iterable (tuple, set, ...), se retorna el objecto sin ordenar.``
    - ``reverse``: Si es True, se ordenara de forma descendente.
    - ``prettyPrint``: Si es True, se imprimirá el objeto ordenado de forma estructurada con ``dumps()``.

    NOTE: Si el objeto no es iterable pero ``prettyPrint`` es True, se retornara el objeto sin ordenar pero mediante el metodo ``dumps().``
    """
    if isinstance(obj, dict):
        ord = _pformat(_OrderedDict(obj), indent=4)    #sorted(obj.items(), key=lambda x: x[0], reverse= reverse)
        if prettyPrint:
            return _pformat(dict(ord), indent=4, sort_dicts=True)
        return ord
    elif isinstance(obj, list):
        ord = sorted(obj, reverse= reverse)
        if prettyPrint:
            return _dumps(ord, indent=4)
        return ord
    elif isinstance(obj, tuple):
        ord = tuple(sorted(obj, reverse= reverse))
        if prettyPrint:
            return _dumps(ord, indent=4)
        return ord
    else:
        if prettyPrint:
            return _dumps(obj, indent=4)
        return obj


def sortByType(object: anyCallable, hierarchy: list[type] = [int, float, str, bool]) -> Any | str | anyCallable:
    """Ordena un objecto de tipo iterable mediante una jerarquía u orden de elementos.
    - Si el objeto no es iterable, se retorna el elemento.

    NOTA: ``Este metodo utiliza un algoritmo de clasificacion algo tedioso en terminos de ejecucción y que es propenso a no ser exacto``
    """
    if not isinstance(hierarchy, list):
        return cFormatter(f"[PARAMS TYPE ERROR]: {_Fore.YELLOW}La jerarquía debe ser una lista de tipos o un tipo.", color= "red")
    elif isinstance(hierarchy, list) and len(hierarchy) <= 0:
        return cFormatter("[PARAMS TYPE ERROR]: La jerarquía debe contener al menos un tipo.", color="red")         
    elif not all(isinstance(x, type) for x in hierarchy):
        return cFormatter("[PARAMS TYPE ERROR]: La jerarquía debe contener solo tipos de datos.", color="red")
    else:
        if not isinstance(object, dict):
            #Creamos una lista para agrupar los elementos en listas segun su tipo.
            #Convertir la lista de listas separada de cada tipo en una sola con los corchetes eliminados 
            clasifier = []
            for typ in hierarchy:
                clasifier.append(sorted(filter(lambda x: isinstance(x, typ), object)))
            type_weight = [x for sublist in clasifier for x in sublist]
            a = [f for f in object if not f in type_weight]
            final = object.__class__(type_weight+a)
            return final
        else:
            try:
                return sorted(object, key=lambda x: (x is not None, "" if isinstance(x, _Number) else type(x).__name__, x))
            except:
                return object
        
        
def sensiblePrint(
    objectOrCode: type | anyCallable,
    indent: int = 4,
) -> None:
    """
    Imprime un objecto con colores segun el tipo de valores que contiene.
    NOTA: Si el objecto no es un iterable, se devolverá el objecto.

    ### Importante:
    Si el objecto es un diccionario y contiene otro diccionario, solo se imprimirá como un diccionario sin colorear sus claves-valores.
    """
    _COLORS = {
        "keys": _Fore.YELLOW,
        "values": _Fore.GREEN,
        "tuples": _Fore.BLUE,
        "sets": _Fore.CYAN,
        "lists": _Fore.MAGENTA,
        "dicts": _Fore.LIGHTBLUE_EX,
        "others": _Fore.LIGHTWHITE_EX,
        "bool": _Fore.LIGHTGREEN_EX,
        "numbers": _Fore.LIGHTRED_EX,
        "none": _Fore.LIGHTYELLOW_EX,
    }
    indent = " " * indent

    if isinstance(objectOrCode, dict):
        print("\n{\t")
        for k,v in objectOrCode.items():
            if isinstance(v, dict):
                print(f"{indent}{_COLORS['keys']}{k}: {_COLORS['dicts']}{v}{_Fore.RESET}")
            elif isinstance(v, list):
                print(f"{indent}{_COLORS['keys']}{k}: {_COLORS['lists']}{v}{_Fore.RESET}")
            elif isinstance(v, tuple):
                print(f"{indent}{_COLORS['keys']}{k}: {_COLORS['tuples']}{v}{_Fore.RESET}")
            elif isinstance(v, set):
                print(f"{indent}{_COLORS['keys']}{k}: {_COLORS['sets']}{v}{_Fore.RESET}")
            elif isinstance(v, bool):
                print(f"{indent}{_COLORS['keys']}{k}: {_COLORS['bool']}{v}{_Fore.RESET}")
            elif isinstance(v, int):
                print(f"{indent}{_COLORS['keys']}{k}: {_COLORS['numbers']}{v}{_Fore.RESET}")
            elif isinstance(v, float):
                print(f"{indent}{_COLORS['keys']}{k}: {_COLORS['numbers']}{v}{_Fore.RESET}")
            elif isinstance(v, str):
                print(f"{indent}{_COLORS['keys']}{k}: {_COLORS['values']}{v}{_Fore.RESET}")

            else:
                print(f"{indent}{_COLORS['keys']}{k}:{_COLORS['none']}{v}{_Fore.RESET}")
        print("}\n")
        return None
    elif isinstance(objectOrCode, list) or isinstance(objectOrCode, tuple):
        print("\n[\t" if isinstance(objectOrCode, list) else "\n(\t")
        for v in objectOrCode:
            if isinstance(v, dict):
                print(f"{indent}{_COLORS['dicts']}{v}{_Fore.RESET}")
            elif isinstance(v, list):
                print(f"{indent}{_COLORS['lists']}{v}{_Fore.RESET}")
            elif isinstance(v, tuple):
                print(f"{indent}{_COLORS['tuples']}{v}{_Fore.RESET}")
            elif isinstance(v, set):
                print(f"{indent}{_COLORS['sets']}{v}{_Fore.RESET}")
            elif isinstance(v, int):
                print(f"{indent}{_COLORS['numbers']}{v}{_Fore.RESET}")
            elif isinstance(v, float):
                print(f"{indent}{_COLORS['numbers']}{v}{_Fore.RESET}")
            elif isinstance(v, str):
                print(f"{indent}{_COLORS['values']}{v}{_Fore.RESET}")
            elif isinstance(v, bool):
                print(f"{indent}{_COLORS['bool']}{v}{_Fore.RESET}")
            else:
                print(f"{indent}{_COLORS['none']}{v}{_Fore.RESET}")
        print("]\n" if isinstance(objectOrCode, list) else ")\n")
        return None
    else:
        return objectOrCode


def get_key(rawDict: dict, value: anyCallable):
    if isinstance(rawDict, dict):
        for k, v in rawDict.items():
            if v == value:
                return k
            continue
        else:
            return cFormatter(f"{_Fore.RED}[PARAMS TYPE ERROR]: {_Fore.YELLOW}El valor '{value}' no existe en el diccionario.{_Fore.RESET}", color= "red")
    else:
        return cFormatter(f"[TYPE ERROR]: {_Fore.YELLOW}El parametro | dict | debe ser un diccionario.{_Fore.RESET}")


def ftime(tformat: str, time:  _datetime | _t.struct_time, braces: tuple[bool, bool] = (False, False), separator: str = " ", color: str = None) -> str:
    """Formatea una fecha o hora a un formato determinado.
    ## Parámetros
    - ``format``: Formato de la fecha a formatear.
        - NOTE: Se puede especificar el formato de la fecha como tipo de formato ``e.g: date | time (ver tipos de formatos validos abajo)`` o directamente como el formato de la fecha.
    - ``time``: Fecha o hora a formatear.
        - NOTE: El tiempo debe estar pasado en SEGUNDOS DESDE LA EPOCA, da igual con que metodo sea si se pasan los segundos desde la epoca.
    - ``braces``: Englobar entre brackets la fecha y la hora. Si ambos son True, la fecha y la hora se englobarán. ``e.g: [dd/mm/yyyy] [hh:mm:ss]``

    Los formatos disponibles son:
    - ``date``: Formatea la fecha a ``dd/mm/yyyy``.
    - ``time``: Formatea la hora a ``hh:mm:ss``.
    - ``time_short``: Formatea la hora a ``hh:mm``.
    - ``year``: Formatea la fecha a ``yyyy``.
    - ``month``: Formatea la fecha a ``mm``.
    - ``day``: Formatea la fecha a ``dd``.
    - ``hour``: Formatea la hora a ``hh``.
    - ``datetime``: Formatea la fecha y hora a ``dd/mm/yyyy hh:mm:ss``.
    - ``datetime_short``: Formatea la fecha y hora a ``dd/mm/yyyy hh:mm``.
    - ``datetime_short_2``: Formatea la fecha y hora a ``yyyy/mm/dd hh``.
    """

    def _parser(fmt: str) -> str:
        dfmt = _fmts[fmt]
        if not separator in vsep:
            return cFormatter(f"[PARAMS TYPE ERROR]: {_Fore.YELLOW}El parametro | separator | debe ser un string.{_Fore.RESET}", color= "red")
        if dfmt.find(" "):
            data, time = dfmt[:dfmt.find(" ")], dfmt[dfmt.find(" ")+1:]
            if braces[0]:
                fmt = f"[{data}]{separator}{time}"
                return fmt
            elif braces[1]:
                fmt = f"{data}{separator}[{time}]"
                return fmt
            elif braces[0] and braces[1]:
                fmt = f"[{data}]{separator}[{time}]"
                return fmt
            else:
                fmt = f"{data}{separator}{time}"
                return fmt
        else:
            if any(braces):
                fmt = f"[{dfmt}]"
                return fmt
            else:
                return dfmt

    _fmts = {
        "date": "%d/%m/%Y",
        "year": "%Y",
        "month": "%m",
        "day": "%d",
        "hour": "%H",
        "time_short": "%H:%M",
        "time": "%H:%M:%S",
        "datetime": "%d/%m/%Y %H:%M:%S",
        "datetime_short": "%d/%m/%Y %H:%M"
    }
    vsep = ["|", ",", ";", " ", "-","\n", "\t", "\r"]

    if not tformat in _fmts.keys():
        return cFormatter(f"[PARAMS TYPE ERROR]: {_Fore.YELLOW}El parametro [format] tiene que ser un formato válido.\nFormatos validos: {[f for f in _fmts]}{_Fore.RESET}", color= "red")
    elif braces and not isinstance(braces, tuple) or isinstance(braces, tuple) and len(braces) != 2:
        return cFormatter(f"[PARAMS TYPE ERROR]: {_Fore.YELLOW}El parametro [braces] tiene que ser una tupla de dos valores.{_Fore.RESET}", color= "red")
    elif braces and not all(not isinstance(b, bool) for b in braces):
        return cFormatter(f"[PARAMS TYPE ERROR]: {_Fore.YELLOW}El parametro [braces] tiene que ser una tupla de dos valores.{_Fore.RESET}", color= "red")
    elif not isinstance(separator, str) and separator is not None or not separator in vsep:
        return cFormatter(f"[PARAMS TYPE ERROR]: {_Fore.YELLOW}El parametro [separator] tiene que ser un string.\nFormatos validos: {[f for f in vsep]}{_Fore.RESET}", color= "red")

    mf = _parser(tformat)
    masterfmt = _t.strftime(mf, _t.localtime(time) if not isinstance(time, _t.struct_time) else time)
    if color:
        return cFormatter(masterfmt, color)
    else:
        return masterfmt


#! ARREGLAR
def createTimer(inThread: bool = True, countdown: int = None, color: str = None, inBackEnd: bool = False) -> object | _Thread | None:
    """Crea un timer/cronometro devolviendo un objeto de tipo ``Clock``
    ### Importante
    - Esta funcion devuelve un objeto ``Clock``. Esto quiere decir que para activar el cronometro se deberá utilizar los metodos de la clase para activarlo,
    en este caso ``initTimer()``

    ## Parametros:
    - ``inThread (bool) = False:`` Si se especifica como True, el cronometro se ejecuta en un Thread independiente.
        - NOTE: Si ``inThread`` es True, el timer/cronometro se ejecutara en un thread y ``NO SE PODRÁ DETENER`` a menos que cierres la terminal.
    - ``countdown (int) = None:`` Cuenta regresiva del cronometro (realiza una CUENTA ATRAS de x tiempo). 
        - NOTE: Si no se especifica, el cronometro se inicia en 0 y es progresiva.
    - ``color (str) = None :`` Color del cronometro, si se desea. Predeterminadamente se printea en Blanco.
    - ``inBackEnd (bool) = False:`` Si se especifica como True, el cronometro no se printea en pantalla y se guarda en una variable.
        - NOTE: Si ``iBackEnd`` es True, debera utilizar ``view()`` para visualizar el cronometro.
    
    ## Uso:         
        
        Properties:
            - ``timer.active:`` Si el cronometro esta activo/corriendo.
    - ``With countdown running in Thread:``\n
    >>> timer = createTimer(countdown=10, inThread=True, color="red")
    >>> timer.iniTimer()
    >>> timer.pauseTimer()
    ---------------------------------------------

    - ``To initialise the timer:``\n
    >>> timer.iniTimer()
    ---------------------------------------------

    - ``To pause the timer:``\n
    >>> timer.pauseTimer()
    ---------------------------------------------

    - ``To active the timer (if time was paused):``\n
        - NOTE: ``This method also will work if the timer have not been initialised.``\n
    >>> timer.activeTimer()
    ---------------------------------------------

    - ``To reset the timer: (The timer must have already been initialised)``\n
    >>> timer.resetTimer()
    ---------------------------------------------


    ### NOTE: "El cronometro funciona con un bucle el cual hace un ``print`` por cada segundo que pasa.
    """

    class Clock:
        def __init__(self, refresh_timer_ms: int = 500):
            self. clockRefresh = refresh_timer_ms
            self._initTime = _datetime.now()
            self._active = False

        @property
        def active(self):
            return self._active

        def _calc_passed_time_format(self):
            passed_seconds = (_datetime.now() - self._initTime).total_seconds()
            return self._primitive_timer(int(passed_seconds))
            
        def _primitive_timer(self, segundos):
            horas = int(segundos / 60 / 60)
            segundos -= horas*60*60
            minutos = int(segundos/60)
            segundos -= minutos*60
            return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

        def view(self):
            "Muestra el proceso del cronometro si el mismo esta activo y se ha pasado True al argumeto ``inBackEnd``"
            if self._active and inBackEnd:
                return self.Thread.run()
            else:
                return None
        
        def iniTimer(self):
            """Inicia el cronometro.
            - Si el cronometro ya esta activo, no se inicia nuevamente.
            - Si ``inBackEnd`` es True, el cronometro no se printea en pantalla y se guarda en una variable que se actualiza cada 500 ms.
                - Si desea ver el estado del cronometro, utilice ``view()``."""
            if inBackEnd:
                self._active = True
                self._initTime = _datetime.now()
                self.Thread = _Thread(target=lambda: self._calc_passed_time_format())
                self.Thread.start()
            else:
                self._active = True
                try:
                    while self._active:
                        if color:
                            print(cFormatter(self._calc_passed_time_format(), color= color), end= "\r")
                        else:
                            print(self._calc_passed_time_format(), end= '\r')
                except KeyboardInterrupt:
                    self._active = False
                    print(cFormatter(f"\n[TIMER STOPPED]: El cronometro ha sido detenido.", color="yellow"))
                
        def pauseTimer(self):
            """Pausa el cronometro si esta activo, sino no hará nada y devolverá ``None``"""
            if self.active:
                self._initTime = _datetime.now()
                self._active = False
            else:
                return None
        def activeTimer(self):
            """Activa el cronometro si esta pausado.\nTambien lo hace si esta parado pero es mejor utilizar el metodo ``.timer()``"""
            if self.active:
                pass
            else:
                self._active = True
                return self._calc_passed_time_format()

        def resetTimer(self):
            """Restablece el cronometro a 0"""
            if self._active:
                self._initTime = _datetime.now()
                print(cFormatter("El cronometro se ha reseteado", color= _Fore.GREEN))
            else:
                return print(self.ClockErrorMsg)
    return Clock()
     