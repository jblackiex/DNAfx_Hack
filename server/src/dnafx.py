import logging
import traceback
import asyncio
from ENV import ENV
from channel_manager import ChannelManager
from time import sleep

async def main():
    try:
        # keyboard hook to close the program

        ENV.init_config()
        IOhub = ChannelManager()
        await asyncio.gather(IOhub.receive_socket(), IOhub.receive_keyboard(), IOhub.send_usbhid(), IOhub.send_gpio())
    except Exception as e:
        raise e

if __name__ == "__main__":
    tryagain = 0
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\rKeyboard interrupt received. Exiting.")
        exit(0)
    except Exception as e:
        error_str = f"Error: {str(e)}" 
        print(error_str)
        logging.error(traceback.format_exc())
        if tryagain < 3:
            sleep(2)
            tryagain += 1
            print(f"Retrying... ({tryagain}/3)")
            asyncio.run(main())
        else:
            exit(1)
        # asyncio.run(main())


