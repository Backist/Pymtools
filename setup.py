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


setup(
    name="hikari",
    version=__version__,
    description="Miscellaneous tools for Python3 to improve and boost your code",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    author=__author__,
    python_requires=">=3.10.0,<3.11",
    packages=find_namespace_packages(include=["misctools*"]),
    install_requires=parse_reqf("requirements.txt"),
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