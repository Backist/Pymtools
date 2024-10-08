import json as _json
import csv as _csv
import yaml as _yaml
from pprint import pformat as _pformat
from pathlib import Path as _Path
from xmltodict import parse as _parse
from toml import dump as _dump

from .misc import validatePath, sensiblePrint, _Fore, _Path

try:
    from xml.dom import minidom as _minidom
except ImportError:
    raise ImportError("No se puede importar xml.dom.minidom")


__all__ = (
    "ex2csv","ex2json","ex2yaml","ex2xml","ex2toml",
    "json2csv","json2xml","json2yaml","json2toml",
    "xml2csv","xml2json","xml2yaml","xml2toml",
    # "csv2json","csv2yaml","csv2toml","csv2xml",
    # "toml2json","toml2csv","toml2yaml","toml2xml"
)


def ex2csv(data, filename: str = "data.csv", **kwargs):
    # sourcery skip: raise-specific-error
    """Exporta una diccionario de datos a un archivo csv.
    
    ## Parametros:
    - ``data (Type["T"]):`` lista de datos a exportar.
        - NOTA: Los datos deben ser de tipo list, dict, tuple, set, str.
    - ``filename (str):`` nombre del archivo a exportar.
    - ``kwargs (dict):`` parametros adicionales para la funcion ``_csv.writer``.

    ### Errores:
    - Si el formato de datos no es valido, una ``Exception`` sera lanzada.
    """

    filename += ".csv" if not filename.endswith(".csv") else None
    if not isinstance(data, dict):
        raise Exception(f"{_Fore.RED}El formato de datos no es valido.{_Fore.RESET}")
    with open(filename, "w") as csvfile:
        writer = _csv.writer(csvfile, delimiter=',', lineterminator='\n', **kwargs)
        for row, value in data.items():
            writer.writerow([row, value])
        csvfile.close()

def ex2json(data, indent: int = 4,filename: str = "data.json", **kwargs):
    """Exporta una diccionario de datos a un archivo json.
    
    ## Parametros:
    - ``data (Type["T"]):`` lista de datos a exportar.
        - NOTA: Los datos deben ser de tipo list, dict, tuple, set, str.
    - ``indent (int):`` cantidad de espacios a mostrar.
    - ``filename (str):`` nombre del archivo a exportar.
    - ``kwargs (dict):`` parametros adicionales para la funcion ``json.dump``.
    """
    filename += ".json" if not filename.endswith(".json") else None
    if not isinstance(data, dict):
        raise Exception(f"{_Fore.RED}El formato de datos no es valido.{_Fore.RESET}")
    with open(filename, "w") as jsonfile:
        _json.dump(data, jsonfile, indent=indent, **kwargs)
        jsonfile.close()

def ex2yaml(data, filename: str = "data.yaml"):
    """Exporta un diccionario de datos a un archivo yaml
    """
    filename += ".yaml" if not filename.endswith(".yaml") else None
    if not isinstance(data, dict):
        raise Exception(f"{_Fore.RED}El formato de datos no es valido.{_Fore.RESET}")
    with open(filename, "w") as yamlfile:
        _yaml.dump(
            data, 
            yamlfile,
            allow_unicode=True, 
            default_flow_style=False, 
            encoding= 'utf-8', 
            sort_keys=True, 
            explicit_start= True, 
            explicit_end= True,
        )
        yamlfile.close()

def ex2xml(data, filename: str = "data.xml", defaultroot: str = "data"):
    """Exporta un diccionario de datos a un archivo xml"""
    filename += ".xml" if not filename.endswith(".xml") else None
    if type(defaultroot) is not str:
        raise Exception(f"{_Fore.RED}La etiqueta raíz del archivo debe ser una string y no ser mayor a 100 caracteres{_Fore.RESET}")
    if not isinstance(data, dict):
        raise Exception(f"{_Fore.RED}El formato de datos no es valido.{_Fore.RESET}")

    root = _minidom.Document()
    xml = root.createElement(defaultroot)
    root.appendChild(xml)

    for key in data.keys():
        if isinstance(data[key], dict):
            ...
        productChild = root.createElement("item")
        productChild.setAttribute("key", key)
        productChild.setAttribute("value",  str(data[key]))
        xml.appendChild(productChild)
    xml_str = root.toprettyxml(indent ="\t", encoding="utf-8", newl="\n") 
    
    with open(filename, "w") as xmlfile:
        xmlfile.write(xml_str.decode("utf-8"))
        xmlfile.close()
        
    
def ex2toml(data, filename: str = "data.toml", **kwargs):
    """Exporta un diccionario de datos a un archivo toml"""
    if not isinstance(data, dict):
        raise Exception(f"{_Fore.RED}El formato de datos no es valido.{_Fore.RESET}")
    with open(filename, "w") as tomlfile:
        _dump(data, tomlfile)
        tomlfile.close()


def json2csv(filepath: _Path, filename: str = "data.csv", delimiter: str = ",", lineterminator: str = "\n"):
    """Exporta un archivo _json a un archivo csv"""
    if not filename.endswith(".csv"):
        print(f"{_Fore.YELLOW}[Convertion Type Warning] El nombre del archivo debe terminar con '.csv'. Se ha agreagado automaticamente.{_Fore.RESET}.")
        filename += ".csv"
    if validatePath(filepath):
        with open(filepath, "r") as _jsonfile:
            data = _json.load(_jsonfile)
            ex2csv(data, filename=filename, delimiter=delimiter, lineterminator=lineterminator)
            _jsonfile.close()
    else:
        return Exception("Error al convertir el archivo. La ruta no es valida.")

def json2yaml(filepath: _Path, filename: str = "data.yaml"):
    """Exporta un archivo _json a un archivo yaml"""
    if not filename.endswith(".yaml"):
        print(f"{_Fore.YELLOW}[Convertion Type Warning] El nombre del archivo debe terminar con '._yaml'. Se ha agreagado automaticament{_Fore.RESET}.")
        filename += ".yaml"
    if validatePath(filepath):
        with open(filepath, "r") as _jsonfile:
            data = _json.load(_jsonfile)
            ex2yaml(data, filename=filename)
            _jsonfile.close()
    else:
        return Exception("Error al convertir el archivo. La ruta no es valida.")

def json2xml(filepath: _Path, filename: str = "data.xml", defaultroot: str | None = "data"):
    """Exporta un archivo _json a un archivo xml"""
    if not filename.endswith(".xml"):
        print(f"{_Fore.YELLOW}[Convertion Type Warning] El nombre del archivo debe terminar con '.xml'. Se ha agreagado automaticamente.{_Fore.RESET}.")
        filename += ".xml"
    if validatePath(filepath):
        with open(filepath, "r") as _jsonfile:
            data = _json.load(_jsonfile)
            ex2xml(data, filename=filename, defaultroot=defaultroot)
            _jsonfile.close()
    else:
        return Exception("Error al convertir el archivo. La ruta no es valida.")

def json2toml(filepath: _Path, filename: str = "data.toml"):
    """Exporta un archivo _json a un archivo toml"""
    if not filename.endswith(".toml"):
        print(f"{_Fore.YELLOW}[Convertion Type Warning] El nombre del archivo debe terminar con '.toml'. Se ha agreagado automaticamente{_Fore.RESET}.")
        filename += ".toml"
    if validatePath(filepath):
        with open(filepath, "r") as _jsonfile:
            data = _json.load(_jsonfile)
            ex2toml(data, filename=filename)
            _jsonfile.close()
    else:
        return Exception("Error al convertir el archivo. La ruta no es valida.")

def yaml2csv(filepath: _Path, filename: str = "data.csv", delimiter: str = ",", lineterminator: str = "\n"):
    """Exporta un archivo yaml a un archivo csv"""
    if not filename.endswith(".csv"):
        print(f"{_Fore.YELLOW}[Convertion Type Warning] El nombre del archivo debe terminar con '.csv'. Se ha agreagado automaticamente.{_Fore.RESET}.")
        filename += ".csv"
    if validatePath(filepath):
        with open(filepath, "r") as yamlfile:
            data = _yaml.load(yamlfile, Loader=_yaml.FullLoader)
            ex2csv(data, filename=filename, delimiter=delimiter, lineterminator=lineterminator)
            yamlfile.close()
    else:
        return Exception("Error al convertir el archivo. La ruta no es valida.")

def yaml2json(filepath: _Path, filename: str = "data.json"):
    """Exporta un archivo _yaml a un archivo json"""
    if not filename.endswith(".json"):
        print(f"{_Fore.YELLOW}[Convertion Type Warning] El nombre del archivo debe terminar con '._json'. Se ha agreagado automaticamente{_Fore.RESET}.")
        filename += ".json"
    if validatePath(filepath):
        with open(filepath, "r") as yamlfile:
            data = _yaml.load(yamlfile, Loader=_yaml.FullLoader)
            ex2json(data, filename=filename)
            yamlfile.close()
    else:
        return Exception("Error al convertir el archivo. La ruta no es valida.")

def yaml2xml(filepath: _Path, filename: str = "data.xml", defaultroot: str | None = "data"):
    """Exporta un archivo _yaml a un archivo xml"""
    if not filename.endswith(".xml"):
        print(f"{_Fore.YELLOW}[Convertion Type Warning] El nombre del archivo debe terminar con '.xml'. Se ha agreagado automaticamente.{_Fore.RESET}.")
        filename += ".xml"
    if validatePath(filepath):
        with open(filepath, "r") as yamlfile:
            data = _yaml.load(yamlfile, Loader=_yaml.FullLoader)
            ex2xml(data, filename=filename, defaultroot=defaultroot)
            yamlfile.close()
    else:
        return Exception("Error al convertir el archivo. La ruta no es valida.")

def yaml2toml(filepath: _Path, filename: str = "data.toml"):
    """Exporta un archivo _yaml a un archivo toml"""
    if not filename.endswith(".toml"):
        print(f"{_Fore.YELLOW}[Convertion Type Warning] El nombre del archivo debe terminar con '.toml'. Se ha agreagado automaticamente{_Fore.RESET}.")
        filename += ".toml"
    if validatePath(filepath):
        with open(filepath, "r") as yamlfile:
            data = _yaml.load(yamlfile, Loader=_yaml.FullLoader)
            ex2toml(data, filename=filename)
            yamlfile.close()
    else:
        return Exception("Error al convertir el archivo. La ruta no es valida.")

def xml2csv(filepath: _Path, filename: str = "data.csv", delimiter: str = ",", lineterminator: str = "\n"):
    """Exporta un archivo xml a un archivo csv"""
    if not filename.endswith(".csv"):
        print(f"{_Fore.YELLOW}[Convertion Type Warning] El nombre del archivo debe terminar con '._csv'. Se ha agreagado automaticamente{_Fore.RESET}.")
        filename += ".csv"
    if validatePath(filepath):
        with open(filepath, "r") as xmlfile:
            data = _parse(xmlfile.read(), encoding="utf-8", xml_declaration=False)
            ex2csv(data, filename=filename, delimiter=delimiter, lineterminator=lineterminator)
            xmlfile.close()
    else:
        return Exception("Error al convertir el archivo. La ruta no es valida.")

def xml2json(filepath: _Path, filename: str = "data.json"):
    """Exporta un archivo xml a un archivo json"""
    if not filename.endswith(".json"):
        print(f"{_Fore.YELLOW}[Convertion Type Warning] El nombre del archivo debe terminar con '.json'. Se ha agreagado automaticamente{_Fore.RESET}.")
        filename += ".json"
    if validatePath(filepath):
        with open(filepath, "r") as xmlfile:
            data = _parse(xmlfile.read(), encoding="utf-8", xml_declaration=False)
            ex2json(data, filename=filename)
            xmlfile.close()
    else:
        return Exception("Error al convertir el archivo. La ruta no es valida.")

def xml2yaml(filepath: _Path, filename: str = "data.yaml"):
    """Exporta un archivo xml a un archivo yaml"""
    if not filename.endswith(".yaml"):
        print(f"{_Fore.YELLOW}[Convertion Type Warning] El nombre del archivo debe terminar con '.yaml'. Se ha agreagado automaticamente{_Fore.RESET}.")
        filename += ".yaml"
    if validatePath(filepath):
        with open(filepath, "r") as xmlfile:
            data = _parse(xmlfile.read(), encoding="utf-8", xml_declaration=False)
            ex2yaml(data, filename=filename)
            xmlfile.close()
    else:
        return Exception("Error al convertir el archivo. La ruta no es valida.")

def xml2toml(filepath: _Path, filename: str = "data.toml"):
    """Exporta un archivo xml a un archivo toml"""
    if not filename.endswith(".toml"):
        print(f"{_Fore.YELLOW}[Convertion Type Warning] El nombre del archivo debe terminar con '.toml'. Se ha agreagado automaticamente{_Fore.RESET}.")
        filename += ".toml"
    if validatePath(filepath):
        with open(filepath, "r") as xmlfile:
            data = _parse(xmlfile.read(), encoding="utf-8", xml_declaration=False)
            ex2toml(data, filename=filename)
            xmlfile.close()
    else:
        return Exception("Error al convertir el archivo. La ruta no es valida.")


if __name__ == "__main__":
    testdict = {
        "test": "test",
        "test2": "test2",
        "test3": "test3",
        "test4": "test4",
        "test5": "test5",
        "test6": "test6",
        "test7": "test7",
        "test8": "test8",
        "test9": "test9",
        "test10": "test10",
        "test11": "test11",
        "test12": "test12",
        "test13": "test13",
        "test14": "test14",
        "test15": "test15",
        "test16": {"stest2": "stest2", "stest3": "stest3", "stest4": {"stest4": "stest4"}}, 
    }
    ex2csv(testdict)
    ex2json(sensiblePrint(testdict))
    ex2yaml(testdict)
    ex2xml(testdict)
    ex2toml(testdict)
    print("Exportaciones exitosas.")
    
    
