import socket
from communication_channel import CommunicationChannel

class SocketChannel(CommunicationChannel):
    """Implementation of Socket communication channel."""
    
    def __init__(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow immediate reuse of the socket
        
        # listen for incoming connections on all network interfaces
        s.bind(('0.0.0.0', 12345))
        s.listen(10)
        return "Received data from Socket"        

    def send(self, message: str) -> None:
        print(f"Sending via Socket: {message}")
    
    def receive(self) -> str:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow immediate reuse of the socket
        # s.bind(('192.168.1.18', 12345))
        s.bind(('0.0.0.0', 12345))
        s.listen(10)
        return "Received data from Socket"