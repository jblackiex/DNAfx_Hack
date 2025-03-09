import logging
import traceback
import usb.core
import usb.util
import asyncio
import socket
from json import JSON
from ENV import ENV
from channel_manager import ChannelManager
from server.src.keyboardinput_channel import KeyboardInputChannel
from server.src.socket_channel import SocketChannel
from usbhid_channel import USBHIDChannel

# Listen for outgoing communication and send the selected command
async def output_loop():
    last_preset = "0"
    effects = JSON.get_json("effects.json")
    while True:
        try:
            message_output = IOhub.receive_message()
            
            # set an input timeout of 4 second if the user doesn't input anything
            if effect.lower() == 'q':
                print("Exiting...")
                break
            if effect.lower() == 'aux':
                print("Aux mode selected")
                effect = input("Enter the effect index/name to select: ")
            if effect.lower() == 's': # Socket mode
                print("Socket mode selected")
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow immediate reuse of the socket
                # s.bind(('192.168.1.18', 12345))
                s.bind(('0.0.0.0', 12345))
                s.listen(10)
                conn, addr = s.accept()
                print(f"Connection from {addr}")
                while True:
                    effect = conn.recv(1024)
                    if not effect:
                        break
                    print(f"Received: {effect.decode()}, length: {len(effect)}")
                    effect = effect[:-1].decode()
                    break
            if effect == "": # If press enter, select the next effect
                effect = str(int(last_preset) + 2)
            elif not effect.isdigit() and effect.upper() not in effects:
                print("effect name not found, want to add it? (y/n)")
                add = input()
                if add.lower() == 'y':
                    print("Enter the effect index command whose name you want to assign: ")
                    effect_index = input()
                    effects.update({effect.upper(): effects[str(int(effect_index) - 1)]})
                    JSON.set_json(effects)
                continue
            elif not effect.isdigit() and effect.upper() in effects:
                send_effect(effect.upper(), effects[effect.upper()])
                continue
            elif not effect.isdigit() or int(effect) not in range(1, len(effects)):
                print("Invalid input. Please enter a valid effect index/name.")
                continue

            effect = str(int(effect) - 1)
            effect_command = effects[effect]
            send_effect(effect, effect_command)
            last_preset = effect
        except usb.core.USBError as e:
            print(f"USB Error: {e}")
            break
        except Exception as e:
            print(f"Error: {e}")
            break


async def main():
    try:
        ENV.init_config()
        IOhub = ChannelManager()
        await asyncio.gather(IOhub.receive_socket(), IOhub.receive_keyboard(), IOhub.send_usbhid(), IOhub.send_gpio())
    except Exception as e:
        raise e

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        error_str = f"Error: {str(e)}" 
        print(error_str)
        logging.error(traceback.format_exc())
        exit(1)


