from output_channel import OutputChannel
from ENV import ENV

class GPIOChannel(OutputChannel):
    """Implementation of GPIO output channel."""
    
    def send(self, data: str, last_preset: list) -> None:
        if (ENV.get("USE_GPIO") == "ON"):
            print(f"Sending via GPIO: next preset {data}")