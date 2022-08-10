from setuptools import setup, find_namespace_packages
from _pckmd import *


def long_description():
    with open("README.md") as fp:
        return fp.read()

def parse_reqf(path):
    try:
        with open(path) as fp:
            dependencies = (d.strip() for d in fp.read().split("\n") if d.strip())
            return [d for d in dependencies if not d.startswith("#")]
    except (FileNotFoundError, PermissionError, IOError) as e:
        return e


VERSION = __version__
NAME = __name__
AUTHOR = __author__
EMAIL = __email__
STATUS = __status__
DESCRIPTION = __description__
LONG_DESCRIPTION = long_description()
LICENSE = __license__
PYTHON_REQUERIMENTS = ">=3.10.0,<3.11"
PACKAGES = find_namespace_packages(include=["misctools*"])
PKG_REQUERIMENTS = parse_reqf("requirements.txt")


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    license=LICENSE,
    python_requires=PYTHON_REQUERIMENTS,
    packages=PACKAGES,
    install_requires=PKG_REQUERIMENTS,
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: Spanish",
        "Programming Language :: Python :: 3.10"
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Typing :: Typed",
    ],
)

#python setup.py sdist bdist_wheel
#pip install twine
#twine upload dist/<compressed_library>/<folder_name>.whl