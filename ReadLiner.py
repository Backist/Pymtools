from pathlib import Path
from logging import warning #, info, critical, error
from os.path import getsize

from mmap import mmap

from PathValidator import *

__all__ = ["readlines"]

def readlines(StrOrPath: Path | str) -> list[int]:
    """Lee las lineas de un archivo y devuelve el numero de lineas.\n
    ``list[0]`` -> Total lines\n
    ``list[1]`` -> Total lines without White lines\n
    ``list[2]`` -> White lines
    """
    if ValidatePath(StrOrPath):
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
        return ValidatePath(StrOrPath)