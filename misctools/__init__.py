"""
### Metadata Information:
------------------------
library: ``misctools``
author: ``Backist``


## Distribution of the library:
-------------------------
Miscellaneous tools to improve the code quality.

The library contains the following distributions:
    - Modules:
        - ``misctools.misc:`` Miscellaneous tools.
        - ``misctools.opsys:`` System functions and file functions.
        - ``misctools.net:`` Network functions.
        - ``misctools.colors:`` Color functions.
        - ``misctools.ext:`` External tools with no specific purpose.

## Common errors and warnings:
-----------------------------
- This library is not intended to be used in POSIX systems, this is because not all methods are currently supported in POSIX systems 
(due to some system operations).
- For example, this library natively uses the ``Path`` class from the ``pathlib`` module, but it is not recommended to use the ``pathlib`` module in POSIX systems.

#### NOTE:
- The library is currently under development and is still in a premature state, however the maintenance of the library is active and new features and functions
will be released in future versions with a shorter turnaround time. If you have encountered a problem, error or bug do not hesitate to contact the author
of the library to try to fix those bugs in the shortest possible time.
"""

__SUPPORTED_VERSIONS__: list[str]= [
    "3.10.2",
    "3.10.3",
    "3.10.4",
    "3.10.5",
    "3.10.6",
    "3.10.7",
]

from platform import system as _system, python_version as _python_version
import sys as _sys

if _system() != "Windows":
    #   raise ImportError
    _sys.stderr("Esta biblioteca no está pensada para ser utilizada en sistemas POSIX, esto se debe a que no todos los métodos están actualmente soportados en sistemas POSIX (debido a algunas operaciones del sistema).")
if not _python_version() in __SUPPORTED_VERSIONS__:
    raise ImportError(f"La librería no puede funcionar en versiones menores a {__SUPPORTED_VERSIONS__[0]}")
else:
    _sys.setrecursionlimit(10000)
    try:
        from .colors import *
        from .misc import *
        from .net import *
        from .opsys import *
        from .exports import * 
        from .ext import * 
    except ModuleNotFoundError as notferr:
        raise ImportError(f"Algo fue mal a la hora de importar modulos de manera interna. Error con el modulo: {notferr.__traceback__}")
    except ImportError as imperr:
        raise ImportError(f"La librería ha detectado un error al importar el siguiente modulo: {imperr}")
    """
    De esta manera, si alguien importa la librería de manera absoluta (import misctools) tendrá todos los metodos y clases de todos los metodos de la librería 
    cargados.

    - Ejemplo 1 (con los modulos importados en el __init__):
       >>> import misctools
       >>> misctools.validatePath() -> funcionará

    - Ejemplo 2 (sin importarlos):
        >>> import misctools
        >>> misctools.validatePath() -> No funcionará
        >>> en su lugar habrá que hacer -> misctools.misc.validatePath()
    """