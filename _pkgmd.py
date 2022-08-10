"""Package metadata."""


__all__: tuple[str, ...] = (
    "__author__",
    "__description__",
    "__autrepo__",
    "__repository__",
    "__copyright__",
    "__license__",
    "__version__",
    "__maintainer__",
    "__email__",
    "__status__",
)

try:
    from typing_extensions import Final
except ImportError:
    from typing import Final


__author__: Final[str] = "Backist"
__description__: Final[str] = "Miscellaneous tools for Python3 to improve and boost your code"
__repository__: Final[str] = "https://github.com/Backist/Misctools"
__autrepo__: Final[str] = "https://github.com/Backist"
__copyright__: Final[str] = "Copyright 2022-Present Backtist"
__license__: Final[str] = "None At the moment"
__version__: Final[str] = "0.1.1"
__maintainer__: Final[str] = "Backist"
__email__: Final[str] = "alvarodrumer54@gmail.com"
__status__: Final[str] = "Planning"
