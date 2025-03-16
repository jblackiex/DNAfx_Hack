from socket_channel import SocketChannel
from keyboardinput_channel import KeyboardChannel
import asyncio

class ChannelData:
    """Store and manage data for input channels."""
    def __init__(self):
        # make a list big enough to store the data
        self.channeldata = [""]
        self.event_channeldata_received = asyncio.Event()

        self.channels = {
            "Keyboard": KeyboardChannel(),
            "Socket": SocketChannel()
        }
    
    async def receive_from(self, channel: str) -> None:
        await self.channels[channel].receive_on(self.channeldata, self.event_channeldata_received)

    async def get_data(self) -> str:
        await self.event_channeldata_received.wait()
        self.event_channeldata_received.clear()
        return self.channeldata[0]