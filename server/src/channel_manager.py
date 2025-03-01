from ENV import ENV
from communication_channel import CommunicationChannel
from usbhid_channel import USBHIDChannel
from socket_channel import SocketChannel
from gpio_channel import GPIOChannel
from keyboardinput_channel import KeyboardInputChannel
# import socket

class ChannelManager:
    def __init__(self, input_channel: str = "keyboard", output_channel: str = "usbhid"):
        self.input_channel = self._get_channel(input_channel)
        self.output_channel = self._get_channel(output_channel)

    def _get_channel(self, channel_type: str) -> CommunicationChannel:
        """Factory method to get the correct channel implementation."""
        channels = {
            "USBHID": USBHIDChannel,
            "Keyboard": KeyboardInputChannel,
            "Socket": SocketChannel,
            "GPIO": GPIOChannel
        }
        if channel_type not in channels:
            raise ValueError(f"Invalid channel type: {channel_type}")
        return channels[channel_type]()

