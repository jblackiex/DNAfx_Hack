import usb.core
import usb.util
from communication_channel import CommunicationChannel
from ENV import ENV

class USBHIDChannel(CommunicationChannel):
    """Implementation of USB HID communication channel."""
    
    def __init__(self):
        # Find the USB device using vendor and product IDs from the environment variables
        device = usb.core.find(idVendor=ENV.get("VENDOR_ID"), idProduct=ENV.get("PRODUCT_ID"))

        if device is None:
            raise ValueError("Device not found")

        # Reset the device to ensure it starts in a clean state
        # This is useful for reinitializing the device in case it was previously in use
        device.reset()

        # If the device is currently controlled by the OS kernel, detach it
        # This allows our script to take direct control of the USB device
        if device.is_kernel_driver_active(0):
            device.detach_kernel_driver(0)

        # Configure the USB device with its default settings
        # This sets up endpoints, interfaces, and other communication parameters
        # Necessary before any communication can occur
        device.set_configuration()

    def send(self, message: str) -> None:
        print(f"Sending via USBHID: {message}")
    
    def receive(self) -> str:
        return "Received data from USBHID"