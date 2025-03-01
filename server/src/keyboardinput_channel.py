from communication_channel import CommunicationChannel

class KeyboardInputChannel(CommunicationChannel):
    """Implementation keyboardinput communication channel."""
    
    def send(self, message: str) -> None:
        print(f"Sending via USBHID: {message}")
    
    def receive(self) -> str:
        return "Received data from USBHID"