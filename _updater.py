def update_reqs(dependencies: list[str] | str):
    """
    Add some dependencies or dependency into ``requeriments.py``.
    """
    if isinstance(dependencies, str):
        dependencies = [dependencies]
    with open("requeriments.txt", "r+") as reqf:
        for dep in dependencies:
            if dep.strip() in reqf.read().strip().splitlines():
                return Exception("La dependencia ya existe en el archivo")
            else:
                reqf.write(f"{dep}\n")
        reqf.close()

            
        
