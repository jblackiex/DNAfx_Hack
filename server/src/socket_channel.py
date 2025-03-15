import socket
import asyncio
from input_channel import InputChannel

class SocketChannel(InputChannel):
    """Implementation of Socket input channel."""
    
    @classmethod
    async def receive_on(cls, channeldata: list, event_data_received: asyncio.Event) -> None:
        # Instead of asyncio.run(), use await
        await cls.server(channeldata, event_data_received)

    @classmethod
    async def server(cls, channeldata: list, event_data_received: asyncio.Event) -> None:
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.setblocking(False)  # No blocking calls
            server_socket.bind(("0.0.0.0", 12345))
            server_socket.listen(5)  # Maximum 5 clients

            loop = asyncio.get_running_loop()

            while True:
                client_socket, addr = await loop.sock_accept(server_socket)  # No blocking call
                print(f"Connected from {addr}")
                asyncio.create_task(cls.handle_client(client_socket, channeldata, event_data_received))  # Handle client in background
        except Exception as e:
            raise e

    @classmethod
    async def handle_client(cls, client_socket, channeldata: list, event_data_received: asyncio.Event) -> None:
        loop = asyncio.get_running_loop()

        while True:
            print("Receiving data...")
            cls.data = await loop.sock_recv(client_socket, 64)  # Reading 64 bytes at a time, no blocking call
            print("Data received:", cls.data.decode())
            if not cls.data.decode():
                print("No data received." + cls.data.decode())
                break
            channeldata[0] = [cls.data.decode()]
            print("Data event set:", cls.data.decode())
            event_data_received.set()
