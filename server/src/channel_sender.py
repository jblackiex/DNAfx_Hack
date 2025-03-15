from usbhid_channel import USBHIDChannel
from gpio_channel import GPIOChannel
from JSON import JSON
from ENV import ENV
class ChannelSender:
    def __init__(self):
        self.last_preset = ["0"]
        self.channels = {
            "USBHID": USBHIDChannel(),
            "GPIO": GPIOChannel()
        }

    async def send_to(self, channel: str, data: str) -> None:
        try:
            self.channels[channel].send(data, self.last_preset)
            print("Enter a command(name/index) to send: ")
        except Exception as e:
            print(f"Error: {e}")
            raise(f"Error: {e}")