import time as t
from colorama import Fore
from pathlib import Path
from os.path import getmtime, splitext, getsize, getatime, getctime

from chardet import detect

from funcs import *


__all__ = ["getInfo", "getSize"]


def getSize(filePathOrStr: Path | str):
    if validatePath(filePathOrStr):
        return round(getsize(filePathOrStr)/1000, 2)
    else:
        return

def getInfo(filePathOrStr: Path | str) -> dict:
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
            print(f"{cFormatter(k, color= Fore.LIGHTYELLOW_EX)}: {cFormatter(finfo[k] ,color= Fore.LIGHTWHITE_EX)}")
    else:
        return validatePath(filePathOrStr)