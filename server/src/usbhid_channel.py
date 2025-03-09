import usb.core
import usb.util
from server.src.input_channel import CommunicationChannel
from ENV import ENV

class USBHIDChannel(CommunicationChannel):
    """Implementation of USB HID communication channel."""
    
    def __init__(self):
        # Find the USB self.device using vendor and product IDs from the environment variables
        self.device = usb.core.find(idVendor=ENV.get("VENDOR_ID"), idProduct=ENV.get("PRODUCT_ID"))

        if self.device is None:
            raise ValueError("self.device not found")

        # Reset the self.device to ensure it starts in a clean state
        # This is useful for reinitializing the self.device in case it was previously in use
        # self.device.reset()

        # If the self.device is currently controlled by the OS kernel, detach it
        # This allows our script to take direct control of the USB self.device
        if self.device.is_kernel_driver_active(0):
            self.device.detach_kernel_driver(0)

        # Configure the USB self.device with its default settings
        # This sets up endpoints, interfaces, and other communication parameters
        # Necessary before any communication can occur
        self.device.set_configuration()

    async def send(self, preset: str) -> None:
        try:
            for _ in range(2): # Send the command twice to respect bInterval of 2ms
                self.device.write(ENV.get("OUT_ENDPOINT"), preset)
            print(f"Sending via USBHID: {preset}")
            # print(f"Effect {effect} selected")
        except usb.core.USBError as e:
            print(f"USB Error: {e}")
    
    async def receive(self) -> str:
        return "Received data from USBHID"