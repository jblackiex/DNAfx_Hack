from input_channel import InputChannel
import asyncio

class OtgChannel(InputChannel):
    """Implementation of OTG input channel."""
    def __init__(self):
        pass

    async def receive_on(cls, channeldata: list, event_data_received: asyncio.Event = None) -> None:
        pass