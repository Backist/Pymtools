import json as _json
import csv as _csv
import yaml as _yaml
from pprint import pformat
from pathlib import Path
from xmltodict import parse
from toml import dump

from .misc import validatePath

try:
    from xml.dom import minidom
except ImportError:
    print("No se puede importar xml.dom.minidom")


__all__ = (
    "ex2csv",
    "ex2json",
    "ex2yaml",
    "ex2xml",
    "ex2toml",
    "json2csv",
    "json2xml",
    "json2yaml",
    "xml2csv",
    "xml2json",
    "xml2yaml"
)


def ex2csv(data, filename: str = "data.csv", **kwargs):
    """Exporta una diccionario de datos a un archivo _csv.
    
    ## Parametros:
    - ``data (Type["T"]):`` lista de datos a exportar.
        - NOTA: Los datos deben ser de tipo list, dict, tuple, set, str.
    - ``filename (str):`` nombre del archivo a exportar.
    - ``kwargs (dict):`` parametros adicionales para la funcion ``_csv.writer``.

    ### Errores:
    - Si el formato de datos no es valido, una ``Exception`` sera lanzada.
    """
    if not isinstance(data, dict):
        raise Exception("El formato de datos no es valido.")
    else:
        with open(filename, "w") as _csvfile:
            writer = _csv.writer(_csvfile, delimiter=',', lineterminator='\n', **kwargs)
            for row, value in data.items():
                writer.writerow([row, value])
            _csvfile.close()

def ex2json(data, indent: int = 4,filename: str = "data.json", **kwargs):
    """Exporta una diccionario de datos a un archivo _json.
    
    ## Parametros:
    - ``data (Type["T"]):`` lista de datos a exportar.
        - NOTA: Los datos deben ser de tipo list, dict, tuple, set, str.
    - ``indent (int):`` cantidad de espacios a mostrar.
    - ``filename (str):`` nombre del archivo a exportar.
    - ``kwargs (dict):`` parametros adicionales para la funcion ``_json.dump``.
    """
    if not isinstance(data, dict):
        raise Exception("El formato de datos no es valido.")
    else:
        with open(filename, "w") as _jsonfile:
            _json.dump(data, _jsonfile, indent=indent, **kwargs)
            _jsonfile.close()

def ex2yaml(data, filename: str = "data.yaml"):
    """Exporta un diccionario de datos a u archivo _yaml"""
    if not isinstance(data, dict):
        raise Exception("El formato de datos no es valido.")
    else:
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

def ex2xml(data, filename: str = "data.xml", defaultroot: str | None = "data"):
    """Exporta un diccionario de datos a un archivo xml"""
    if not isinstance(data, dict):
        raise Exception("El formato de datos no es valido.")

    root = minidom.Document()
    xml = root.createElement("data")    
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
        raise Exception("El formato de datos no es valido.")
    else:
        with open(filename, "w") as tomlfile:
            dump(data, tomlfile)
            tomlfile.close()


def json2csv(filepath: Path, filename: str = "dump2json.csv", delimiter: str = ",", lineterminator: str = "\n"):
    """Exporta un archivo _json a un archivo csv"""
    if not filename.endswith(".csv"):
        print("El nombre del archivo debe terminar con '.csv'. Se ha agreagado automaticamente.")
        filename += ".csv"
    if validatePath(filepath):
        with open(filepath, "r") as _jsonfile:
            data = _json.load(_jsonfile)
            ex2csv(data, filename=filename, delimiter=delimiter, lineterminator=lineterminator)
            _jsonfile.close()
    else:
        return Exception("Error al convertir el archivo. La ruta no es valida.")

def json2yaml(filepath: Path, filename: str = "dump2json.yaml"):
    """Exporta un archivo _json a un archivo yaml"""
    if not filename.endswith(".yaml"):
        print("El nombre del archivo debe terminar con '._yaml'. Se ha agreagado automaticamente.")
        filename += ".yaml"
    if validatePath(filepath):
        with open(filepath, "r") as _jsonfile:
            data = _json.load(_jsonfile)
            ex2yaml(data, filename=filename)
            _jsonfile.close()
    else:
        return Exception("Error al convertir el archivo. La ruta no es valida.")

def json2xml(filepath: Path, filename: str = "dump2json.xml", defaultroot: str | None = "data"):
    """Exporta un archivo _json a un archivo xml"""
    if not filename.endswith(".xml"):
        print("El nombre del archivo debe terminar con '.xml'. Se ha agreagado automaticamente.")
        filename += ".xml"
    if validatePath(filepath):
        with open(filepath, "r") as _jsonfile:
            data = _json.load(_jsonfile)
            ex2xml(data, filename=filename, defaultroot=defaultroot)
            _jsonfile.close()
    else:
        return Exception("Error al convertir el archivo. La ruta no es valida.")

def json2toml(filepath: Path, filename: str = "dump2json.toml"):
    """Exporta un archivo _json a un archivo toml"""
    if not filename.endswith(".toml"):
        print("El nombre del archivo debe terminar con '.toml'. Se ha agreagado automaticamente.")
        filename += ".toml"
    if validatePath(filepath):
        with open(filepath, "r") as _jsonfile:
            data = _json.load(_jsonfile)
            ex2toml(data, filename=filename)
            _jsonfile.close()
    else:
        return Exception("Error al convertir el archivo. La ruta no es valida.")

def yaml2csv(filepath: Path, filename: str = "dump2yaml.csv", delimiter: str = ",", lineterminator: str = "\n"):
    """Exporta un archivo yaml a un archivo csv"""
    if not filename.endswith(".csv"):
        print("El nombre del archivo debe terminar con '.csv'. Se ha agreagado automaticamente.")
        filename += ".csv"
    if validatePath(filepath):
        with open(filepath, "r") as yamlfile:
            data = _yaml.load(yamlfile, Loader=_yaml.FullLoader)
            ex2csv(data, filename=filename, delimiter=delimiter, lineterminator=lineterminator)
            yamlfile.close()
    else:
        return Exception("Error al convertir el archivo. La ruta no es valida.")

def yaml2json(filepath: Path, filename: str = "dump2yaml.json"):
    """Exporta un archivo _yaml a un archivo json"""
    if not filename.endswith(".json"):
        print("El nombre del archivo debe terminar con '._json'. Se ha agreagado automaticamente.")
        filename += ".json"
    if validatePath(filepath):
        with open(filepath, "r") as yamlfile:
            data = _yaml.load(yamlfile, Loader=_yaml.FullLoader)
            ex2json(data, filename=filename)
            yamlfile.close()
    else:
        return Exception("Error al convertir el archivo. La ruta no es valida.")

def yaml2xml(filepath: Path, filename: str = "dump2yaml.xml", defaultroot: str | None = "data"):
    """Exporta un archivo _yaml a un archivo xml"""
    if not filename.endswith(".xml"):
        print("El nombre del archivo debe terminar con '.xml'. Se ha agreagado automaticamente.")
        filename += ".xml"
    if validatePath(filepath):
        with open(filepath, "r") as yamlfile:
            data = _yaml.load(yamlfile, Loader=_yaml.FullLoader)
            ex2xml(data, filename=filename, defaultroot=defaultroot)
            yamlfile.close()
    else:
        return Exception("Error al convertir el archivo. La ruta no es valida.")

def yaml2toml(filepath: Path, filename: str = "dump2yaml.toml"):
    """Exporta un archivo _yaml a un archivo toml"""
    if not filename.endswith(".toml"):
        print("El nombre del archivo debe terminar con '.toml'. Se ha agreagado automaticamente.")
        filename += ".toml"
    if validatePath(filepath):
        with open(filepath, "r") as yamlfile:
            data = _yaml.load(yamlfile, Loader=_yaml.FullLoader)
            ex2toml(data, filename=filename)
            yamlfile.close()
    else:
        return Exception("Error al convertir el archivo. La ruta no es valida.")

def xml2csv(filepath: Path, filename: str = "dump2xml.csv", delimiter: str = ",", lineterminator: str = "\n"):
    """Exporta un archivo xml a un archivo csv"""
    if not filename.endswith(".csv"):
        print("El nombre del archivo debe terminar con '._csv'. Se ha agreagado automaticamente.")
        filename += ".csv"
    if validatePath(filepath):
        with open(filepath, "r") as xmlfile:
            data = parse(xmlfile.read(), encoding="utf-8", xml_declaration=False)
            ex2csv(data, filename=filename, delimiter=delimiter, lineterminator=lineterminator)
            xmlfile.close()
    else:
        return Exception("Error al convertir el archivo. La ruta no es valida.")

def xml2json(filepath: Path, filename: str = "dump2xml.json"):
    """Exporta un archivo xml a un archivo json"""
    if not filename.endswith(".json"):
        print("El nombre del archivo debe terminar con '.json'. Se ha agreagado automaticamente.")
        filename += ".json"
    if validatePath(filepath):
        with open(filepath, "r") as xmlfile:
            data = parse(xmlfile.read(), encoding="utf-8", xml_declaration=False)
            ex2json(data, filename=filename)
            xmlfile.close()
    else:
        return Exception("Error al convertir el archivo. La ruta no es valida.")

def xml2yaml(filepath: Path, filename: str = "dump2xml.yaml"):
    """Exporta un archivo xml a un archivo yaml"""
    if not filename.endswith(".yaml"):
        print("El nombre del archivo debe terminar con '.yaml'. Se ha agreagado automaticamente.")
        filename += ".yaml"
    if validatePath(filepath):
        with open(filepath, "r") as xmlfile:
            data = parse(xmlfile.read(), encoding="utf-8", xml_declaration=False)
            ex2yaml(data, filename=filename)
            xmlfile.close()
    else:
        return Exception("Error al convertir el archivo. La ruta no es valida.")

def xml2toml(filepath: Path, filename: str = "dump2xml.toml"):
    """Exporta un archivo xml a un archivo toml"""
    if not filename.endswith(".toml"):
        print("El nombre del archivo debe terminar con '.toml'. Se ha agreagado automaticamente.")
        filename += ".toml"
    if validatePath(filepath):
        with open(filepath, "r") as xmlfile:
            data = parse(xmlfile.read(), encoding="utf-8", xml_declaration=False)
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
    ex2json(testdict)
    ex2yaml(testdict)
    ex2xml(testdict)
    ex2toml(testdict)
    print("Exportaciones exitosas.")
    # print()
    # _json2xml(filepath="C:\\Users\\Usuario\\Desktop\\Programacion\\MiscTools\\data.json")
    # _json2_yaml(filepath="C:\\Users\\Usuario\\Desktop\\Programacion\\MiscTools\\data.json")
    # _json2toml(filepath="C:\\Users\\Usuario\\Desktop\\Programacion\\MiscTools\\data.json")
    # _yaml2xml(filepath="C:\\Users\\Usuario\\Desktop\\Programacion\\MiscTools\\data.yaml")
    # _yaml2_json(filepath="C:\\Users\\Usuario\\Desktop\\Programacion\\MiscTools\\data.yaml")
    # _yaml2toml(filepath="C:\\Users\\Usuario\\Desktop\\Programacion\\MiscTools\\data.yaml")
    # xml2_csv(filepath="C:\\Users\\Usuario\\Desktop\\Programacion\\MiscTools\\data.xml")
    # xml2_json(filepath="C:\\Users\\Usuario\\Desktop\\Programacion\\MiscTools\\data.xml")
    # xml2_yaml(filepath="C:\\Users\\Usuario\\Desktop\\Programacion\\MiscTools\\data.xml")
    # xml2toml(filepath="C:\\Users\\Usuario\\Desktop\\Programacion\\MiscTools\\data.xml")
    
    
