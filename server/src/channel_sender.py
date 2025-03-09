from usbhid_channel import USBHIDChannel
from gpio_channel import GPIOChannel
class ChannelSender:
    def __init__(self):
        self.channels = {
            "USBHID": USBHIDChannel(),
            "GPIO": GPIOChannel()
        }