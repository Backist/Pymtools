import pathlib
import os.path

from pathlib import Path


__all__ = ["ValidatePath"]



def ValidatePath(path: Path | str) -> bool:
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
