import socket

def get_ip() -> str:
    """Retorna la ip del sistema"""
    return socket.gethostbyname(socket.gethostname())


if __name__ == "__main__":
    ...