def update_reqs(dependencies: list[str] | str, remove: list[str] | str = []):
    """
    Add some dependencies or dependency into ``requeriments.py``.
    """
    if isinstance(dependencies, str):
        dependencies = [dependencies]
    if isinstance(remove, str):
        remove = [remove]
    with open("requeriments.txt", "r+") as reqf:
        for dep in dependencies:
            if dep.strip() in reqf.read().strip().splitlines():
                return Exception("La dependencia ya existe en el archivo")
            else:
                reqf.write(f"{dep}\n")
            lines = reqf.readlines()
            if len(remove) > 0:
                with open("requeriments.txt", "w") as reqf:
                    for line in lines:
                        if line.strip('\n') in remove:
                            continue
                        reqf.write(line)
        reqf.close()
       
        
