from socket_channel import SocketChannel
from keyboardinput_channel import KeyboardChannel
import asyncio

class ChannelData:
    """Store and manage data for communication channels."""
    def __init__(self):
        self.channeldata = []
        self.event_channeldata_received = asyncio.Event()

        self.channels = {
            "Keyboard": KeyboardChannel(),
            "Socket": SocketChannel()
        }
    
    async def receive_from(self, channel: str) -> None:
        self.channels[channel].receive_on(self.channeldata[0], self.event_channeldata_received)

    async def get_data(self) -> str:
        self.event_channeldata_received.wait()
        self.event_channeldata_received.clear()
        return self.channeldata[0]