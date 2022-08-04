from collections import namedtuple
from pathlib import Path
from random import choice
from os.path import getsize
from typing import TypeVar, Optional, Type
from datetime import datetime
from mmap import mmap, ACCESS_READ #, ACCESS_WRITE
from threading import Thread

from colorama import Fore, Back, Style

__all_: list[str] = [
    "cFormatter",
    "readlines",
    "validatePath", 
    "is_email", 
    "get_key", 
    "formatted_time", 
    "createTimer"
]


_notNone = TypeVar("_notNone", int, str, float, bool, set, list, tuple, dict)

def cFormatter(
    string: str,
    color: str, 
    style: Optional[str] = None, 
    background: Optional[str] = None,
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

    colors = vars(Fore)
    styles = vars(Style)
    backgrounds = vars(Back)
    try:
        color = color.upper()
        style = style.upper() if style is not None else None
        background = background.upper() if background is not None else None
        iter_colors = [color.upper() for color in iter_colors] if len(iter_colors) > 0 else []
    except AttributeError:
        return f"{Fore.RED}Los parametros deben ser de tipo: {Fore.YELLOW}color-> str | style-> str | background-> str.{Fore.RESET}"


    if not color in colors.keys():
        suggestions = [ck for ck in colors.keys() if (ck[0] and ck[-1] == color[0] and color[-1]) or 
        (ck[5:][:1] == color[5:][:1] if color.startswith("LIGHT") else ck[:3] == color[:3]) or ck.startswith(color[0])
        ]
        return f"""{Fore.RED}| {color} | no es un color valido.{Fore.RESET}{Fore.BLUE}
        Quisiste decir {[s for s in suggestions if s != "RESET"]}?{Fore.RESET}
        Colores validos: {Fore.LIGHTYELLOW_EX}{[c for c in colors if c != 'RESET']}{Fore.RESET}
        """
    elif background is not None and not background in backgrounds.keys():
        suggestions = [bk for bk in backgrounds.keys() if (bk[0] and bk[-1] == background[0] and background[-1]) or 
        (bk[5:][:1] == background[5:][:1] if background.startswith("LIGHT") else bk[:3] == background[:3]) or bk.startswith(background[0])
        ]
        return f"""{Fore.RED}| {background} | no es un background valido.{Fore.RESET}{Fore.BLUE}
        Quisiste decir {[s for s in suggestions if s != "RESET"]}?{Fore.RESET}
        Backgrounds validos: {Fore.LIGHTYELLOW_EX}{[s for s in backgrounds if s != 'RESET']}{Fore.RESET}
        """
    elif style is not None and not style in styles.keys():
        suggestions = [sk for sk in styles.keys() if sk.startswith(style[0]) or sk.endswith(style[-1]) or [char for char in style if char in sk]]
        return f"""{Fore.RED}| {style} | no es un estilo valido.{Fore.RESET}{Fore.BLUE}
        Quisiste decir {[s for s in suggestions if s != "RESET_ALL"]}?{Fore.RESET}
        Estilos validos: {Fore.LIGHTYELLOW_EX}{[b for b in styles if b != 'RESET_ALL']}{Fore.RESET}
        """
    else:
        if iter_colors:
            ilegal = [x.upper() for x in iter_colors if not x.upper() in colors.keys()]
            #* si algun color no es valido, se guarda en la lista ilegal y si ilegal != 0 se devuelve un mensaje de error con el color invalido
            if len(iter_colors) == 0 or ilegal:
                return f"{Fore.RED}No se ha definido una lista de colores con los que iterar o algun color no es valido.{Fore.RESET}{Fore.LIGHTCYAN_EX}\nColor Error: {[f for f in ilegal]}{Fore.RESET}"
            else:
                if forline:
                    # #* hacemos que la lista de colores se repita tantas lineas de codigo haya (para que zip funcione)
                    # iter_colors += iter_colors * len(er.split("\n"))
                    # lines = []
                    # #* zip nos permite iterar sobre dos listas a la vez (cada elemento de una con el mismo elemento de la otra)
                    #TODO: el metodo parará cuando alguno de las dos listas se acabe
                    # for line, lc in zip(string.split("\n"), iter_colors):
                    #     lines.append(f"{colors[lc]}{line}{Fore.RESET}")
                    iter_colors += iter_colors * len(string.split("\n"))
                    lines = list(map(lambda line, color: f"{colors[color]}{line}{Fore.RESET}", string.split("\n"), iter_colors))
                    return "\n".join([f for f in lines])
                else: 
                    letters = []
                    for chars in string:
                        letters.append(f"{colors[choice(iter_colors)]}{chars}{Fore.RESET}")
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


def readlines(pathfile: Optional[Path | str] = None , text: Optional[str] = None, ToNamedTuple: bool = True) -> tuple[int, int, int] | tuple[tuple, tuple]:
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

    single_tuple = namedtuple("linesTuple", ["Total_Lines", "Total_Lines_Without_White_Lines", "White_Lines"], defaults=[0,0,0])
    single_tuple.__doc__ = """ReadLine namedtuple\n
    DEFAULT VALUES: ``total_lines = != 0, total_lines+white_lines = 0, white_lines = 0``

    ## Elements\n
    ``total_lines`` -> Total lines of the file or text. This never will be 0.\n
    ``total_lines_without_white_lines`` -> Total lines without including white lines.This field can be 0 if single string is passed.
        - NOTE: ``!Maybe this field can not work properly!``
    ``white_lines`` -> Total white lines. This field can be 0.. 
        - NOTE: !If singe line string with spaces is supplied, this field will be 0"
    """
    double_tuple = namedtuple("linesTuple", ["pathfile_lines", "text_lines"])
    double_tuple.__doc__ = """ReadLine namedtuple\n
    This tuple of tuple returns two tuples with the lines of the file and the text.
    """

    pathfile = pathfile if pathfile is not None and isinstance(pathfile, Path) else Path(pathfile) if pathfile is not None else None

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
        with open(pathfile if isinstance(pathfile, Path) else Path(pathfile), "r+b") as file:
            if getsize(file.name) == 0:
                return f"{Fore.YELLOW}[FILE ERROR]: {Fore.YELLOW}El archivo esta vacio.{Fore.RESET}"
            else:
                pass
            mm = mmap(file.fileno(), 0, access=ACCESS_READ)
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
            return f"{Fore.RED}[PARAMS NULL ERROR]: {Fore.YELLOW}Al menos un valor no debe ser None.{Fore.RESET}"
        elif text is not None and not isinstance(text, str) or pathfile is not None and not isinstance(pathfile, Path) or not isinstance(pathfile, str):
            return f"{Fore.RED}[PARAMS TYPE ERROR]: {Fore.YELLOW}Los valores admitidos son: `pathfile': (str | Path) y 'text': (str).{Fore.RESET}"
        else:
            return f"{Fore.RED}[FUNC ERROR]: Algo ha ido mal a la hora de ejecutar la funcion. Revise los parametros.{Fore.RESET}"


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


def is_email(email:str):
    valids = ["gmail.com", "hotmail.com", "outlook.com", "yahoo.com", "live.com", "ymail.com", "mail.com", "protonmail.com"]

    if not email.endswith(".com") and email[email.find("@")+1:]:
        print(cFormatter(f"[PARAMS TYPE ERROR]: {Fore.YELLOW}Parece que el email es valido pero su dominio no termina por '.com' .{Fore.RESET}", color= "red"))
        return False
    elif not email[email.find("@")+1:] in valids or not email.find("@") > 0 or not email.endswith(".com"):
        return False
    else:
        return True


def get_key(rawDict: dict, value: type):
    if isinstance(rawDict, dict):
        for k, v in rawDict.items():
            if v == value:
                return k
    else:
        return cFormatter(f"[TYPE ERROR]: {Fore.YELLOW}El parametro | dict | debe ser un diccionario.{Fore.RESET}")


def formatted_time(format: str, time: str | datetime) -> str:
    ...

def createTimer(time: int, inThread: bool = True, colored: bool = False) -> None:
    """Crea un cronometro que se ejecuta cada ``time`` segundos"""

    class Clock:
        def __init__(self, refresh_timer_ms: int = 500):
            self. clockRefresh = refresh_timer_ms
            self._initTime = datetime.now()
            self._active = False

        @property
        def active(self):
            return self._active if self._active else None

        def _calc_passed_time_format(self):
            passed_seconds = (datetime.now() - self._initTime).total_seconds()
            return self._primitive_timer(int(passed_seconds))
            
        def _primitive_timer(self, segundos):
            horas = int(segundos / 60 / 60)
            segundos -= horas*60*60
            minutos = int(segundos/60)
            segundos -= minutos*60
            return f"{horas:02d}:{minutos:02d}:{segundos:02d}"
        
        def iniTimer(self):
            try:
                while True:
                    self._active = True
                    if colored:
                        random_color = choice([color.upper() for color in vars(Fore).keys() if color != "RESET" or color != "BLACK"])
                        print(cFormatter(self._calc_passed_time_format(), color= random_color), end= "\r")
                    print(self._calc_passed_time_format(), end= '\r')
            except KeyboardInterrupt:
                self._active = False
                print("\n")
                return cFormatter(f"[TIMER STOPPED]: El cronometro ha sido detenido.", color="yellow")
                
        def pauseTimer(self):
            if self.active:
                self._initTime = datetime.now()
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
            if self._active:
                self._initTime = datetime.now()
                print(cFormatter("El cronometro se ha reseteado", color= Fore.GREEN))
            else:
                return print(self.ClockErrorMsg)

    if inThread:
        thread = Thread(target= lambda: Clock(time).iniTimer())
        thread.start()
        return thread
    else:
        return Clock(time)
    

if __name__ == "__main__":

    testr = """Esto es una pequeña prueba.
    Cabezera 1:
        - Ejemplo 1 -> Esto es una breve explicacion de lo que puede llegar a contener este ejemplo.
        - Ejemplo 2 -> Esto es una breve explicacion de lo que puede llegar a contener este ejemplo.
        - Ejemplo 3 -> Esto es una breve explicacion de lo que puede llegar a contener este ejemplo.
        - Ejemplo 4 -> Esto es una breve explicacion de lo que puede llegar a contener este ejemplo.
        Sub-cabecera 1:
            - Ejemplo 1.1 -> Estos son algunos ejemplos de la Sub-cabezera 1.
            - Ejemplo 2.1 -> Estos son algunos ejemplos de la Sub-cabezera 1.
            - Ejemplo 3.1 -> Estos son algunos ejemplos de la Sub-cabezera 1.
            - Ejemplo 4.1 -> Estos son algunos ejemplos de la Sub-cabezera 1.
            Sub-sub-cabezera 1 -> Sin embargo, en la sub-sub-cabecera 1 tenemos algunos ejemplos de demostracion con aproxiamadamente 3 tabulaciones
                - Ejemplo 1.1.1 -> Esto es una breve explicacion de lo que puede llegar a contener este ejemplo.
                - Ejemplo 2.1.1 -> Esto es una breve explicacion de lo que puede llegar a contener este ejemplo.
                - Ejemplo 3.1.1 -> Esto es una breve explicacion de lo que puede llegar a contener este ejemplo.
                - Ejemplo 4.1.1 -> Esto es una breve explicacion de lo que puede llegar a contener este ejemplo.
    Cabezera 2:
        - Ejemplo 1 -> Esto serian algunos ejemplos mas importantes puesto que estan en la segunda cabezera, y, por tanto, segundo elemento principal de esta string.
        - Ejemplo 2 -> Esto serian algunos ejemplos mas importantes puesto que estan en la segunda cabezera, y, por tanto, segundo elemento principal de esta string.
        - Ejemplo 3 -> Esto serian algunos ejemplos mas importantes puesto que estan en la segunda cabezera, y, por tanto, segundo elemento principal de esta string.
        - Ejemplo 4 -> Esto serian algunos ejemplos mas importantes puesto que estan en la segunda cabezera, y, por tanto, segundo elemento principal de esta string.
    -------------------------------------------------------------
    Despedida y finalizacion del texto/docstring:

    Como modo de prueba y finalizacion del texto/docstring,
    Backest.
    """
    print(type(testr))

    e = cFormatter(
        testr,
        color="LIGHTBLUE_EX", 
        iter_colors= ["GREEN", "BLUE", "YELLOW", "CYAN"],
        forline=True
    )
    print(e)
    print(readlines(None,testr))
    e = createTimer(1, inThread=False, colored=True)
    print(e.iniTimer())
