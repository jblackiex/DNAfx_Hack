import asyncio
from ENV import ENV
from channel_data import ChannelData
from channel_sender import ChannelSender
# import socket

class ChannelManager:
    """
        Manages communication channels for sending and receiving messages. This class acts
        as the controller of the MVC pattern. It is responsible for managing the communication
        channels and the data flow between them. It is responsible for sending and receiving
        messages from different channels. It acts as a bridge between the input and output
        channels. It can send messages to one channel and receive messages from another channel.
        Examples:
        - receive from Socket, send to USB HID
        - receive from Keyboard, send through GPIO
        - receive from Keyboard, send through USB HID
    """
    def __init__(self):
        self.channel_data = ChannelData()
        self.channel_sender = ChannelSender()

    async def receive_socket(self):
        # await asyncio.sleep(1.5)
        await self.channel_data.receive_from("Socket")

    async def receive_keyboard(self):
        # await asyncio.sleep(1.5)
        await self.channel_data.receive_from("Keyboard")

    async def send_usbhid(self):
        while True:
            await asyncio.sleep(1.5)
            data = await self.channel_data.get_data()
            await self.channel_sender.send_to("USBHID", data)

    async def send_gpio(self):
        while True:
            await asyncio.sleep(1.5)
            data = await self.channel_data.get_data()
            await self.channel_sender.send_to("GPIO", data)