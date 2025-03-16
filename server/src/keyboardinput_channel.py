import asyncio
import sys
from input_channel import InputChannel

class KeyboardChannel(InputChannel):
    """Implementation of keyboard input communication channel."""
    
    @classmethod
    async def receive_on(cls, channeldata: list, event_data_received: asyncio.Event) -> None:
        """Asynchronously reads user input from the keyboard without using threads."""
        loop = asyncio.get_running_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)
        await loop.connect_read_pipe(lambda: protocol, sys.stdin)
        
        while True:
            print("Enter a command: ")
            user_input = await reader.readline()
            user_input = user_input.decode().strip()
            if user_input.lower() == "exit":  # Exit condition
                break
            channeldata[0] = user_input.strip()
            event_data_received.set()