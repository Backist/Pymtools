
from collections import namedtuple
from functools import lru_cache
from json import dumps, detect_encoding
from pathlib import Path
from os import (getcwd, getlogin, getpid, abort, walk, remove, renames, rename, system, stat, scandir)
from os.path import (getsize, getctime, getatime, getmtime, splitext, join, exists, isdir, isfile, islink, ismount)
import time as t
import platform
import sys

import shutil 

from chardet import detect
from colorama import Fore as _Fore

from .misc import *


def sysInfo() -> str | dict:
    """Retorna un diccionario con la informacion del sistema"""
    sysinf = {
        "platform": platform.platform(),
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "node": platform.node(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "architecture": platform.architecture(),
    }
    finaldict = {}

    for i, v in sysinf.items():
        finaldict[i.capitalize()] = v
    return dumps(finaldict, indent=4)

def pythonInfo() -> dict:
    """Retorna un diccionario con la informacion del sistema"""
    pyinf = {
        "python_version": platform.python_version(),
        "python_compiler": platform.python_compiler(),
        "python_branch": platform.python_branch(),
        "python_implementation": platform.python_implementation(),
        "python_revision": platform.python_revision(),
        "python_version_tuple": platform.python_version_tuple(),
    }
    finaldict = {}
    for i, v in pyinf.items():
        finaldict[i.capitalize()] = v
    return dumps(finaldict, indent= 4)


def get_python_root() -> Path:
    """Retorna el Path del directorio raiz de python"""
    return Path(sys.prefix)


def get_parent_path(relativePath: Path) -> Path:
    """Retorna el path del directorio padre de un path"""
    if isinstance(relativePath,str):
        try:
            relativePath = Path(relativePath)
        except:
            raise Exception("Parece que la ruta no es correcta o no se ha podido procesar")
    elif not validatePath(relativePath):
        raise ValueError("La ruta no existe")
    return relativePath.parent if not relativePath.is_absolute() else relativePath.parent.absolute().resolve(True)  


def get_win_user() -> str:
    """Retorna el usuario del sistema"""
    return getlogin()


def get_winsaved_users() -> list:
    """Retorna los usuarios del equipo mediante el comando ``net users``
    - *NOTA: ``Esta funcion puede ir mal si eres de linux.``
    """
    print(cFormatter("Obteniendo usuarios guardados en el equipo...", color="LIGHTYELLOW_EX"))
    print(cFormatter("[RECOMENDACION]: Puede ser mejor opcion ejecutar 'netplwiz' o 'net user' en el simbolo de sistema (CMD) o Powershell", color="LIGHTYELLOW_EX"))
    return system("net user")


def get_disk_size(diskroot: Path | str | list[Path | str] = "/", toNamedTuple: bool = True, inBytes: bool = False) -> tuple[int | float]:
    """Retorna el tamaño del disco en ``GB``.
        - NOTA: Si desea un tiempo de ejecuccion rapido, use la funcion ``disk_usage()`` del modulo ``shutil``.
    """
    single_tuple = namedtuple("DiskUsageTuple", "Total, Used, Free")
    single_tuple.__doc__ = """"""
    if isinstance(diskroot, str) and not diskroot == "/":
            diskroot = Path(diskroot)
    elif isinstance(diskroot, Path) and not validatePath(diskroot, estrict=True):
        raise TypeError(cFormatter("El parametro | diskroot | debe ser un Path valido.", color="RED"))
    elif isinstance(diskroot, list):
        if len(diskroot) > 5:
            raise RecursionError(cFormatter("Por terminos de recursión solo se puede obtener el tamaño de 5 discos.", color="RED"))
        else:
            vs_list = tuple((map(lambda i: get_disk_size(i, toNamedTuple=toNamedTuple, inBytes=inBytes), diskroot)))
            return vs_list
    total, used, free = shutil.disk_usage(diskroot)
    vs_list = (total // (2**30) if not inBytes else total, used // (2**30) if not inBytes else used, free // (2**30) if not inBytes else free)
    return single_tuple(*vs_list) if toNamedTuple else vs_list


def get_extension(filePathOrStr: Path, wdot: bool = True) -> str | None:
    """Intenta devolver la extension del archivo dado.\n
    La funcion puede devolver ``None`` si no se consigue obtener la extesion del archivo

    ### Parametros
    - ``wdot | (bool -> True)``:   Si ``wdot`` es ``False``, se devuelve la extension del archivo con el punto eliminado
    """

    if validatePath(filePathOrStr):
        if wdot:
            return splitext(filePathOrStr)[1]
        return splitext(filePathOrStr)[1][1:]
    else:
        return validatePath(filePathOrStr)


def get_size(filePathOrStr: Path | str):
    "Devuelve el tamaño total del archivo en ``Bytes``"
    if validatePath(filePathOrStr):
        return round(getsize(filePathOrStr)/1000, 2)
    else:
        return


def get_finfo(filePathOrStr: Path | str, prettyPrint: bool = False) -> dict:
    TIME_FMT = "%Y-%m-%d %H:%M:%S"
    if validatePath(filePathOrStr):
        finfo = {}
        afile = t.strftime(TIME_FMT, t.localtime(getatime(filePathOrStr)))
        mfile = t.strftime(TIME_FMT, t.localtime(getmtime(filePathOrStr)))
        cfile = t.strftime(TIME_FMT, t.localtime(getctime(filePathOrStr)))    #* Devuelve la hora de creacion del archivo
        sfile = getsize(filePathOrStr)
        ext = splitext(filePathOrStr)[1]   #* Divide la ruta en dos, donde el segundo elemento es la extension.
        with open(filePathOrStr, "r+") as file:
            Tobytes = Path(filePathOrStr).read_bytes() if not isinstance(filePathOrStr, Path) else filePathOrStr.read_bytes()
            enc = file.encoding
        finfo["Name"] = file.name
        finfo["Absolute path"] = Path(filePathOrStr).absolute().as_posix() if not isinstance(filePathOrStr, Path) else filePathOrStr.absolute().as_posix()
        finfo["Home directory"] = Path(filePathOrStr).home().as_posix() if not isinstance(filePathOrStr, Path) else filePathOrStr.home().as_posix()
        finfo["Last access"] = afile
        finfo["Last modification"] = mfile
        finfo["Creation data"] = cfile
        finfo["File size"] = f"{bytes2kilobytes(sfile, precision=2)} KB ({kilobytes2megabytes(bytes2kilobytes(sfile, precision=2), precision=2)} MB)"
        finfo["Total lines"] = readlines(filePathOrStr)[0]
        finfo["Extension"] = ext
        finfo["Language"] = get_lang(filePathOrStr) if get_lang(filePathOrStr) is not None else detect(Tobytes).get("language") if detect(Tobytes).get("language") else "Unknown"
        finfo["Encoding"] = enc

        if prettyPrint:
            for k in finfo.keys():
                print(f"{cFormatter(k, color= 'LIGHTYELLOW_EX')}: {cFormatter(finfo[k] ,color= 'LIGHTWHITE_EX')}")
        else:
            return finfo
    else:
        raise ValueError(f"El parametro | filePathOrStr | debe ser un Path valido.")


def get_lang(__file: Path | str) -> str | None:
    if type(__file) is str:
        try:
            __file = Path(__file)
        except:
            raise ValueError(f"La ruta no existe o no se puede abrir")
    elif not __file.exists() or not __file.is_file():
        raise ValueError(f"La ruta no existe existe o no es un archivo")
    _mapped_langs = {
        "txt": "Plain Text",
        "md": "Markdown",
        "py": "Python",
        "js": "JavaScript",
        "tsx": "TypeScript",
        "html": "HTML",
        "css": "CSS",
        "cpp": "C++",
        "java": "JAVA",
        "go": "GO",
        "c": "C Language",
        "lua": "Lua",
        "r": "R",
        "sql": "SQL",
    }
    if get_extension(__file, False) in _mapped_langs.keys():
        return _mapped_langs[get_extension(__file, False).lower()]
    else:
        return


def get_filenc(filePathOrStr: Path | str) -> dict:
    """Intenta detectar la codificacion del archivo."""
    if validatePath(filePathOrStr, estrict=True):
        with open(filePathOrStr, "rb") as file:
            #open it as bytes to avoid problems with encodings
            enc =  detect_encoding(file.read())
        return {"Encoding": enc}
    else:
        raise ValueError("Invalid path")


def is_file(filePathOrStr: Path | str) -> bool:
    """Retorna un boolean si la ruta es un archivo o no."""
    if isinstance(filePathOrStr, str):
        filePathOrStr = Path(filePathOrStr)
    return filePathOrStr.is_file() if isinstance(filePathOrStr, Path) and filePathOrStr.exists() else False


def incwdir(filePathOrStr: Path | str) -> bool:
    """Retorna un boolean si la ruta se encuentra o existe dentro del directorio actual o en un directorio contenido en el directorio actual/raíz.

    NOTE: ``Si la ruta esta contenida en un direcorio dentro del raíz pero una ruta relativa es pasada, se retornará False.``"""
    #TODO: verificar si la ruta esta en el directorio de trabajo o en un directorio contenido en el directorio de trabajo

    if isinstance(filePathOrStr, str):
        try:
            filePathOrStr = Path(filePathOrStr)
        except Exception as e:
            raise ValueError("Invalid Path.\nOriginal Callback: %s" % e)

    if isinstance(filePathOrStr, Path) and not filePathOrStr.exists():
        raise ValueError("Invalid path. The path doesn't exist")

    #? elif not filePathOrStr.is_absolute():
    #?     raise ValueError("Invalid path. Relative path was given and it isn't in the current work directory")

    elif not filePathOrStr.is_absolute():
        filePathOrStr = filePathOrStr.absolute().resolve(True)

    final_path = filePathOrStr.resolve(True)
    for i in scandir(getcwd()):
        if i.is_dir():
            for d in scandir(i.path):
                if str(final_path) == d.path:
                    return True
        elif str(final_path) == i.path:
            return True
    return False


def findCallables(__file: Path, includePrivateMethods: bool = False) -> list[str]:
    """Busca en un archivo todos los elementos que son 'callables' como funciones (asicronas tambien) o clases.
    Metodo útil para actualizar en concreto el metodo __all__ de la libreria.

    ## Parametros:
    - `file`: Path = Ruta
    - `includePrivateMethods`: bool = True -> `Booleano que indica si los metodos y clases privadas tambien se cuentan`

    #### Ejemplo para utilizar este metodo
    
    >>> callableslist = findCallables(<pathfile>)
    >>> #ahora tenemos una lista con todos los metodos o elementos del archivo
    >>> #ahora comparamos si el metodo __all__ del archivo (que contiene una lista o tupla con los elementos que puede ser llamados con *) tiene todos los callables
    >>> if not all(c in __all__ for c in callableslist):
    >>>    __all__.append([c for c in callableslist if not c in __all__])  
    """
    callables = ["def", "async def", "class"]
    nofcalls = []
    _filepath = Path(__file) if not isinstance(__file, Path) else __file
    if not _filepath.is_file():
        raise TypeError(f"{_Fore.RED}La ruta debe contener un archivo o no se encuentra la ruta{_Fore.RESET}")
    try:
        with open(_filepath, "r+", encoding= "utf-8") as f:
            f.seek(0)
            for line in f:
                line = line.rstrip()
                if line.startswith("#"):
                    pass
                elif any(i in line for i in callables):
                    for i in callables:
                        if line.startswith(i):
                            nline = line[len(i)+1:]
                            if nline.startswith("_") and not includePrivateMethods:
                                continue
                            if nline.find("("):
                                nofcalls.append(nline[:nline.find("(")])
                            elif nline.find(":"):
                                nofcalls.append(nline[:nline.find(":")-1])
            f.close()
    except (PermissionError, IOError) as e:
        raise e
    return nofcalls


def is_64bit() -> bool:
    """Retorna un booleano dependiendo de si el sistema es 64 bits"""
    return sys.maxsize > 2**32

def is_32bit() -> bool:
    """Retorna un booleano dependiendo de si el sistema es 32 bits"""
    return sys.maxsize <= 2**32


def bytes2kilobytes(_bytes: int | float, binary: bool = False, precision: int = 4) -> float:
    """Convierte de bytes a kilobytes"""
    return round(_bytes / 1000, precision) if not binary else round(_bytes / 1024, precision)

def bytes2megabytes(_bytes: int | float, binary: bool = False, precision: int = 4) -> float:
    """Convierte de bytes a megabytes"""
    return round(_bytes / (1000**2), precision) if not binary else round(_bytes / (1024**2), precision)

def bytes2gigabytes(_bytes: int | float, binary: bool = False, precision: int = 4) -> float:
    """Convierte de bytes a gigabytes"""
    return round(_bytes / (1000**3), precision) if not binary else round(_bytes / (1024**3), precision)

def bytes2terabytes(_bytes: int | float, binary: bool = False, precision: int = 4) -> float:
    """Convierte de bytes a terabytes"""
    return round(_bytes / (1000**4), precision) if not binary else round(_bytes / (1024**4), precision)


def kilobytes2bytes(_kilobytes: int | float, binary: bool = False, precision: int = 4) -> float:
    """Convierte de kilobytes a bytes"""
    return round(_kilobytes * 1000, precision) if not binary else round(_kilobytes * 1024, precision)

def kilobytes2megabytes(_kilobytes: int | float, binary: bool = False, precision: int = 4) -> float:
    """Convierte de kilobytes a megabytes"""
    return round(_kilobytes / 1000, precision) if not binary else round(_kilobytes / 1024, precision)

def kilobytes2gigabytes(_kilobytes: int | float, binary: bool = False, precision: int = 4) -> float:
    """Convierte de kilobytes a gigabytes"""
    return round(_kilobytes / (1000**2), precision) if not binary else round(_kilobytes / (1024**2), precision)

def kilobytes2terabytes(_kilobytes: int | float, binary: bool = False, precision: int = 4) -> float:
    """Convierte de kilobytes a terabytes"""
    return round(_kilobytes / (1000**3), precision) if not binary else round(_kilobytes / (1024**3), precision)


def megabytes2bytes(_megabytes: int | float, binary: bool = False, precision: int = 4) -> float:
    """Convierte de megabytes a bytes"""
    return round(_megabytes * (1000**2), precision) if not binary else round(_megabytes * (1024**2), precision)

def megabytes2kilobytes(_megabytes: int | float, binary: bool = False, precision: int = 4) -> float:
    """Convierte de megabytes a kilobytes"""
    return round(_megabytes * 1000, precision) if not binary else round(_megabytes * 1024, precision)

def megabytes2gigabytes(_megabytes: int | float, binary: bool = False, precision: int = 4) -> float:
    """Convierte de megabytes a gigabytes"""
    return round(_megabytes / 1000, precision) if not binary else round(_megabytes / 1024, precision)

def megabytes2terabytes(_megabytes: int | float, binary: bool = False, precision: int = 4) -> float:
    """Convierte de megabytes a terabytes"""
    return round(_megabytes / (1000**2), precision) if not binary else round(_megabytes / (1024**2), precision)


def gigabytes2bytes(_gigabytes: int | float, binary: bool = False, precision: int = 4) -> float:
    """Convierte de gigabytes a bytes"""
    return round(_gigabytes * (1000**3), precision) if not binary else round(_gigabytes * (1024**3), precision)

def gigabytes2kilobytes(_gigabytes: int | float, binary: bool = False, precision: int = 4) -> float:
    """Convierte de gigabytes a kilobytes"""
    return round(_gigabytes * (1000**2), precision) if not binary else round(_gigabytes * (1024**2), precision)

def gigabytes2megabytes(_gigabytes: int | float, binary: bool = False, precision: int = 4) -> float:
    """Convierte de gigabytes a megabytes"""
    return round(_gigabytes * 1000, precision) if not binary else round(_gigabytes * 1024, precision)

def gigabytes2terabytes(_gigabytes: int | float, binary: bool = False, precision: int = 4) -> float:
    """Convierte de gigabytes a terabytes"""
    return round(_gigabytes / 1000, precision) if not binary else round(_gigabytes / 1024, precision)


def terabytes2bytes(_terabytes: int | float, binary: bool = False, precision: int = 4) -> float:
    """Convierte de terabytes a bytes"""
    return round(_terabytes * (1000**4), precision) if not binary else round(_terabytes * (1024**4), precision)

def terabytes2kilobytes(_terabytes: int | float, binary: bool = False, precision: int = 4) -> float:
    """Convierte de terabytes a kilobytes"""
    return round(_terabytes * (1000**3), precision) if not binary else round(_terabytes * (1024**3), precision)

def terabytes2megabytes(_terabytes: int | float, binary: bool = False, precision: int = 4) -> float:
    """Convierte de terabytes a megabytes"""
    return round(_terabytes * (1000**2), precision) if not binary else round(_terabytes * (1024**2), precision)

def terabytes2gigabytes(_terabytes: int | float, binary: bool = False, precision: int = 4) -> float:
    """Convierte de terabytes a gigabytes"""
    return round(_terabytes * 1000, precision) if not binary else round(_terabytes * 1024, precision)

def terabytes2petabytes(_terabytes: int | float, binary: bool = False, precision: int = 4) -> float:
    """Convierte de terabytes a petabytes"""
    return round(_terabytes / 1000, precision) if not binary else round(_terabytes / 1024, precision)


def int2binary(n: int) -> int:
    if not isinstance(n, int):
        raise TypeError("Parameter n must be a integer number")
    else:
        return int(bin(n)[2:])

def int2number(n: int) -> int:
    if not isinstance(n, int):
        raise TypeError("Parameter n must be a integer number")
    elif not all(no in [0, 1] for no in n):
        raise TypeError("Invalid binary number: %s" % n)
    dec_num = 0
    for pos, nnumber in enumerate(n[::-1]):
        dec_num += int(nnumber) * 2 ** pos
    return int(dec_num)

__all__ = findCallables(__file__.capitalize())