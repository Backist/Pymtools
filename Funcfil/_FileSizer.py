from os.path import getsize
from pathlib import Path

from ..Funcs.PathValidator import *

__all__ = ["getSize"]

def getSize(filePathOrStr: Path | str):
    if ValidatePath(filePathOrStr):
        return round(getsize(filePathOrStr)/1000, 2)
    else:
        return
