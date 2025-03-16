from abc import ABC, abstractmethod
import asyncio
# Interface for communication channels *(Aux)
# input_output channels should implement this interface
class InputOutputChannel(ABC):
    """Abstract base class for input channels."""

    @abstractmethod
    def receive_on(cls, channeldata: list) -> None:
        pass
    
    @abstractmethod
    def send(self, preset: str, last_preset: list) -> None:
        pass