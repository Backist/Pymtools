import socket

def get_ip() -> str:
    """Retorna la ip del sistema"""
    return socket.gethostbyname(socket.gethostname())

def get_hostname() -> str:
    """Retorna el nombre del host"""
    return socket.gethostname()

def get_mac() -> str:
    return socket.gethostbyaddr(socket.gethostname())[2][0]     # Retorna la mac del host

def get_proto_number(protocol: int) -> str:
    """Retorna el numero de identificacion del protocolo"""
    #Decimal protocools info -> https://es.wikipedia.org/wiki/Anexo:N%C3%BAmeros_de_protocolo_IP
    # 0 to 140 -> active protocols
    # 141 to 255 -> reserved protocols
    number = socket.getprotobyname("icmp")
    return number

def validateIp(ip: str) -> bool:
    """Testea si la ip es valida"""
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

def checkConn() -> bool:
    """Testea la conexion a internet"""
    try:
        e = socket.create_connection(("www.google.com", 80))
        e.close()
        return True
    except OSError:
        return False

if __name__ == "__main__":
    print(get_ip())
    print(get_hostname())
    print(get_mac())
    print(get_proto_number("tcp"))
    print(validateIp(get_ip()))
    print(checkConn())
