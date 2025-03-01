from ENV import ENV
from JSON import JSON

effects = JSON.get_json("effects.json")

# Listen for outgoing communication and send the selected command
def select_effect():
    last_effect = "0"
    while True:
        try:
            # set an input timeout of 4 second if the user doesn't input anything

            effect = input("Enter the index/name to select an effect ('q' to quit, 'h' for help): ")
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
                effect = str(int(last_effect) + 2)
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
            last_effect = effect
        except usb.core.USBError as e:
            print(f"USB Error: {e}")
            break
        except Exception as e:
            print(f"Error: {e}")
            break

def send_effect(effect, effect_command):
    try:
        for _ in range(2): # Send the command twice to respect bInterval of 2ms
            device.write(OUT_ENDPOINT, effect_command)
        print(f"Effect {effect} selected")
    except usb.core.USBError as e:
        print(f"USB Error: {e}")

# Start the interception loop
select_effect()
