"""
### Metadata Information:
------------------------
library: ``misctools``
version: ``0.1``


## Distribution of the library:
-------------------------
Miscellaneous tools to improve the code quality.

The library contains the following distributions:
    - Modules:
        - ``misctools.misc:`` Miscellaneous tools.
        - ``misctools.sysfuncs:`` System functions and file functions.
        - ``misctools.netfuncs:`` Network functions.
        - ``misctools.colorfuncs:`` Color functions.
        - ``misctools.ext:`` External tools with no specific purpose.
    - Sub_packages:
        - ``ICompressor:`` Compression tools with GUI implementation.
        - ``IConverter:`` Conversion tools with GUI implementation.

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


from platform import system as _system, python_version as _python_version
import sys as _sys

if _system() != "Windows":
    #   raise ImportError
    sys.stderr("Esta biblioteca no está pensada para ser utilizada en sistemas POSIX, esto se debe a que no todos los métodos están actualmente soportados en sistemas POSIX (debido a algunas operaciones del sistema).")
if _python_version() < "3.10.2":
    raise ImportError("La librería no puede funcionar en versiones menores a [3.10.2].")
else:
    _sys.setrecursionlimit(10000)
    try:
        from .colorfuncs import *
        from .misc import *
        from .netfuncs import *
        from .sysfuncs import *
        from .ext import *
        from misctools.ICompressor import *
        from misctools.IConverter import *
    except OSError or ImportError as eme:
        raise ImportError(f"No se han podido importar ciertos modulos de la libreria. Informe a su creador de este error: [Error: 100]\nCallback: {eme}")   