from output_channel import OutputChannel

class GPIOChannel(OutputChannel):
    """Implementation of GPIO communication channel."""
    
    def send(self, command: str, command_name: str) -> None:
        print(f"Sending via GPIO: {command_name}")