from abc import ABC, abstractmethod
import asyncio
# Interface for communication channels *(KeyBoard Input, Socket)
# input channels should implement this interface
class InputChannel(ABC):
    """Abstract base class for input channels."""

    @abstractmethod
    async def receive_on(cls, channeldata: list, event_data_received: asyncio.Event = None) -> None:
        pass