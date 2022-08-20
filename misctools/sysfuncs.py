from collections import namedtuple
from json import dumps, dump, detect_encoding
from pathlib import Path
from os import (getcwd, getlogin, getpid, abort, walk, remove, renames, rename, system, stat, scandir, terminal_size, get_terminal_size)
from os.path import (getsize, getctime, getatime, getmtime, splitext, join, exists, isdir, isfile, islink, ismount)
import time as t
import platform
import sys
import os
import shutil 
import psutil

from chardet import detect

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
    return relativePath.absolute().parent if isinstance(relativePath, Path) and relativePath.is_absolute() else cFormatter("El parametro | relative_path | debe ser de tipo Path o ser relativa.")


def get_extension(filePathOrStr: Path) -> str:
    if validatePath(filePathOrStr):
        return splitext(filePathOrStr)[1]
    else:
        return validatePath(filePathOrStr)


def get_win_user() -> str:
    """Retorna el usuario del sistema"""
    return getlogin()


def get_winsaved_users() -> list:
    """Retorna los usuarios del equipo mediante el comando ``net users``
    - *NOTA: ``Esta funcion puede ir mal si eres de linux.``
    """
    print(cFormatter("Obteniendo usuarios guardados en el equipo...", color="LIGHTYELLOW_EX"))
    print(cFormatter("[RECOMENDACION]: Puede ser mejor opcion ejecutar 'netplwiz' o 'net user' en el simbolo de sistema (CMD) o Powershell", color="LIGHTYELLOW_EX"))
    return os.system("net user")

def get_disk_size(diskroot: Path | str | list[Path | str] = "/", toNamedTuple: bool = True, inBytes: bool = False) -> tuple[int | float]:
    """Retorna el tamaño del disco en ``GB``.
        - NOTA: Es recomendable en terminos de tiempo de ejecuccion usar la funcion ``disk_usage()`` del modulo ``shutil``, ya que esta funcion proviene de ese modulo.
    """
    single_tuple = namedtuple("DiskUsageTuple", "Total, Used, Free")
    single_tuple.__doc__ = """"""
    if isinstance(diskroot, str) and not diskroot == "/":
            diskroot = Path(diskroot)
    elif isinstance(diskroot, Path) and not validatePath(diskroot, estrict=True):
        return cFormatter("El parametro | diskroot | debe ser un Path valido.", color="RED")
    elif isinstance(diskroot, list):
        if len(diskroot) > 5:
            return cFormatter("Por terminos recursivos solo se puede obtener el tamaño de 5 discos.", color="RED")
        else:
            vs_list = tuple((map(lambda i: get_disk_size(i, toNamedTuple=toNamedTuple, inBytes=inBytes), diskroot)))
            return vs_list
    total, used, free = shutil.disk_usage(diskroot)
    vs_list = (total // (2**30) if not inBytes else total, used // (2**30) if not inBytes else used, free // (2**30) if not inBytes else free)
    return single_tuple(*vs_list) if toNamedTuple else vs_list

def get_Size(filePathOrStr: Path | str):
    if validatePath(filePathOrStr):
        return round(getsize(filePathOrStr)/1000, 2)
    else:
        return

def is_64bit() -> bool:
    """Retorna un booleano dependiendo de si el sistema es 64 bits"""
    return sys.maxsize > 2**32

def is_32bit() -> bool:
    """Retorna un booleano dependiendo de si el sistema es 32 bits"""
    return sys.maxsize <= 2**32

def bytes2megabytes(bytes: int) -> float:
    """Convierte un numero de bytes a megabytes"""
    return bytes / (2**20)

def bytes2kilobytes(bytes: int) -> float:
    """Convierte un numero de bytes a kilobytes"""
    return bytes / (2**10)

def bytes2gigabytes(bytes: int) -> float:
    """Convierte un numero de bytes a gigabytes"""
    return bytes / (2**30)

def bytes2terabytes(bytes: int) -> float:
    """Convierte un numero de bytes a terabytes"""
    return bytes / (2**40)


# def bytes2mb(bytes: int) -> float:
#     """Convierte un numero de bytes a megabytes"""
#     return bytes / (2**20)

# def bytes2kb(bytes: int) -> float:
#     """Convierte un numero de bytes a kilobytes"""
#     return bytes / (2**10)

# def bytes2gb(bytes: int) -> float:
#     """Convierte un numero de bytes a gigabytes"""
#     return bytes / (2**30)

# def bytes2tb(bytes: int) -> float:
#     """Convierte un numero de bytes a terabytes"""
#     #dar la conversion en terabytes
#     return

# def kb2bytes(kb: float) -> int:
#     """Convierte un numero de kilobytes a bytes"""
#     return kb * (2**10)

# def kb2mb(kb: float) -> int:
#     """Convierte un numero de kilobytes a megabytes"""
#     return kb * (2**20)

# def kb2gb(kb: float) -> int:
#     """Convierte un numero de kilobytes a gigabytes"""
#     return kb * (2**30)

# def kb2tb(kb: float) -> int:
#     """Convierte un numero de kilobytes a terabytes"""
#     return kb * (2**40)


# def mb2bytes(mb: float) -> int:
#     """Convierte un numero de megabytes a bytes"""
#     return mb * (2**20)

# def mb2kb(mb: float) -> int:
#     """Convierte un numero de megabytes a kilobytes"""
#     return mb * (2**10)

# def mb2gb(mb: float) -> int:
#     """Convierte un numero de megabytes a gigabytes"""
#     return mb * (2**30)

# def mb2tb(mb: float) -> int:
#     """Convierte un numero de megabytes a terabytes"""
#     return mb * (2**40)


# def gb2bytes(gb: float) -> int:
#     """Convierte un numero de gigabytes a bytes"""
#     return gb * (2**30)

# def gb2mb(gb: float) -> int:
#     """Convierte un numero de gigabytes a megabytes"""
#     return gb * (2**20)

# def gb2kb(gb: float) -> int:
#     """Convierte un numero de gigabytes a kilobytes"""
#     return gb * (2**10)

# def gb2tb(gb: float) -> int:
#     """Convierte un numero de gigabytes a terabytes"""
#     return gb * (2**40)


def get_finfo(filePathOrStr: Path | str) -> dict:
    TIME_FMT = "%Y-%m-%d %H:%M:%S"
    if validatePath(filePathOrStr):
        finfo = {}
        afile = t.strftime(TIME_FMT, t.localtime(getatime(filePathOrStr)))
        mfile = t.strftime(TIME_FMT, t.localtime(getmtime(filePathOrStr)))
        cfile = t.strftime(TIME_FMT, t.localtime(getctime(filePathOrStr)))    #* Devuelve la hora de creacion del archivo
        sfile = getsize(filePathOrStr)
        ext = splitext(filePathOrStr)[1]   #* Divide la ruta en dos, donde el segundo elemento es la ext.
        with open(filePathOrStr, "r+") as file:
            Tobytes = Path(filePathOrStr).read_bytes() if not isinstance(filePathOrStr, Path) else filePathOrStr.read_bytes()
            enc = file.encoding
        finfo["Name"] = file.name
        finfo["Absolute path"] = Path(filePathOrStr).absolute().as_posix() if not isinstance(filePathOrStr, Path) else filePathOrStr.absolute().as_posix()
        finfo["Home directory"] = Path(filePathOrStr).home().as_posix() if not isinstance(filePathOrStr, Path) else filePathOrStr.home().as_posix()
        finfo["Last access"] = afile
        finfo["Last modification"] = mfile
        finfo["Creation data"] = cfile
        finfo["File size"] = f"{sfile} KB"
        finfo["Total lines"] = readlines(filePathOrStr)[1]
        finfo["Extension"] = ext
        finfo["Language"] = detect(Tobytes).get("language") if detect(Tobytes).get("language") else "Unknown"
        finfo["Encoding"] = enc

        for k in finfo.keys():
            print(f"{cFormatter(k, color= 'LIGHTYELLOW_EX')}: {cFormatter(finfo[k] ,color= 'LIGHTWHITE_EX')}")
    else:
        return validatePath(filePathOrStr)
