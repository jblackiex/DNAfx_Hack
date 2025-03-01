from communication_channel import CommunicationChannel

class SocketChannel(CommunicationChannel):
    """Implementation of Socket communication channel."""
    
    def send(self, message: str) -> None:
        print(f"Sending via Socket: {message}")
    
    def receive(self) -> str:
        return "Received data from Socket"