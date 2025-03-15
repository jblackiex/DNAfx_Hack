from abc import ABC, abstractmethod
import asyncio
# Interface for communication channels *(USBHID, GPIO)
# output channels should implement this interface
class OutputChannel(ABC):
    """Abstract base class for input channels."""

    @abstractmethod
    def send(self, preset: str, preset_name: str) -> None:
        pass