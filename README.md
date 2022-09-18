# Misctools
**Miscellaneous tools to speed up and improve your code.**
- The package is divided by modules that contain functions to diferent related situation

### Modules:
- **misc** - ``General funcs with no clear purpose``
- **opsys** - ``Some util funcs to access and manage system``
- **colors** - ``Util functions to handle color management (conversions, random picker, ...)``
- **net** - ``Some util funcs to extract information about network``
- **ext** - ``Aditional small module to extract the list of colors in a image. Intended to use to study images/patron-color images``
- **exports** - ``Some util funcs to make exports easier. Current langs that can export each other -> [JSON, YAML, CSV, TOML, XML]``

## Install package

### Linux(Posix)
To install the library, do:
- ``pip3 install -U misctools --user`` -> To install the library ONLY in user context
- ``pip3 install -U misctools`` -> To install the library in global context

### Windows (NT):
*Currently the library is not in PyPi.
To install the library with **PyPi & pip**, do:
- ``pip install -U misctools --user`` -> To load the library ONLY in user context
- ``pip install -U misctools`` -> To load the library in global context

- To install with PyPi, do ``pip install -U misctools``
- To install **without** PyPi, do **``pip install -U git+https://github.com/Backist/Misctools``**
    - !! _If u want to install the library without PyPi, then u must have **[GIT](https://git-scm.com/downloads)** installed._
    -  [Install GIT](https://git-scm.com/downloads)

### Exceptions & Errors:
If for any reason you can not install the library via ``PyPi & pip`` you will have to install it manually.
...


- _NOTE: This module have been created to be used in ``Windows | NT systems``, because implemets some functions and methods that couldn't be runned in ``Linux | Posix systems``, this does not mean that some functions can work correctly._

