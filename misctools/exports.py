from toml import dump
import json
import csv
import yaml
try:
    from xml.dom import minidom
except ImportError:
    print("No se puede importar xml.dom.minidom")


def export_to_csv(data, filename: str = "data.csv", **kwargs):
    """Exporta una diccionario de datos a un archivo csv.
    
    ## Parametros:
    - ``data (Type["T"]):`` lista de datos a exportar.
        - NOTA: Los datos deben ser de tipo list, dict, tuple, set, str.
    - ``filename (str):`` nombre del archivo a exportar.
    - ``kwargs (dict):`` parametros adicionales para la funcion ``csv.writer``.

    ### Errores:
    - Si el formato de datos no es valido, una ``Exception`` sera lanzada.
    """
    if not isinstance(data, dict):
        raise Exception("El formato de datos no es valido.")
    else:
        with open(filename, "w") as csvfile:
            writer = csv.writer(csvfile, delimiter=',', lineterminator='\n', **kwargs)
            for row, value in data.items():
                writer.writerow([row, value])
            csvfile.close()

def export_to_json(data, indent: int = 4,filename: str = "data.json", **kwargs):
    """Exporta una diccionario de datos a un archivo json.
    
    ## Parametros:
    - ``data (Type["T"]):`` lista de datos a exportar.
        - NOTA: Los datos deben ser de tipo list, dict, tuple, set, str.
    - ``indent (int):`` cantidad de espacios a mostrar.
    - ``filename (str):`` nombre del archivo a exportar.
    - ``kwargs (dict):`` parametros adicionales para la funcion ``json.dump``.
    """
    if not isinstance(data, dict):
        raise Exception("El formato de datos no es valido.")
    else:
        with open(filename, "w") as jsonfile:
            json.dump(data, jsonfile, indent=indent, **kwargs)
            jsonfile.close()

def export_to_yaml(data, filename: str = "data.yaml"):
    """Exporta un diccionario de datos a u archivo yaml"""
    if not isinstance(data, dict):
        raise Exception("El formato de datos no es valido.")
    else:
        with open(filename, "w") as yamlfile:
            yaml.dump(
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

def export_to_xml(data, filename: str = "data.xml", defaultroot: str | None = "data"):
    """Exporta un diccionario de datos a un archivo xml"""
    if not isinstance(data, dict):
        raise Exception("El formato de datos no es valido.")

    root = minidom.Document()
    xml = root.createElement("data")    
    root.appendChild(xml)

    for key in data.keys():
        if isinstance(data[key], dict):
            ...
        productChild = root.createElement("key")
        productChild.setAttribute("name", key)
        productChild.setAttribute("value",  str(data[key]))
        xml.appendChild(productChild)
    xml_str = root.toprettyxml(indent ="\t", encoding="utf-8", newl="\n") 
    
    with open(filename, "w") as xmlfile:
        xmlfile.write(xml_str)
        xmlfile.close()
        
    
def export_to_toml(data, filename: str = "data.toml", **kwargs):
    """Exporta un diccionario de datos a un archivo toml"""
    if not isinstance(data, dict):
        raise Exception("El formato de datos no es valido.")
    else:
        with open(filename, "w") as tomlfile:
            dump(data, tomlfile)
            tomlfile.close()
    

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
    export_to_csv(testdict)
    export_to_json(testdict)
    export_to_yaml(testdict)
    export_to_xml(testdict, defaultroot=None)
    export_to_toml(testdict)
    print("Exportaciones exitosas.")
