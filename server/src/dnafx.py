import logging
import traceback
import asyncio
from ENV import ENV
from channel_manager import ChannelManager

async def main():
    try:
        # keyboard hook to close the program

        ENV.init_config()
        IOhub = ChannelManager()
        await asyncio.gather(IOhub.receive_socket(), IOhub.receive_keyboard(), IOhub.send_usbhid(), IOhub.send_gpio())
    except Exception as e:
        raise e

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\rKeyboard interrupt received. Exiting.")
        exit(0)
    except Exception as e:
        error_str = f"Error: {str(e)}" 
        print(error_str)
        logging.error(traceback.format_exc())
        exit(1)
        # asyncio.run(main())


