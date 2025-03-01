from communication_channel import CommunicationChannel

class GPIOChannel(CommunicationChannel):
    """Implementation of GPIO communication channel."""
    
    def send(self, message: str) -> None:
        print(f"Sending via GPIO: {message}")
    
    def receive(self) -> str:
        return "Received data from GPIO"