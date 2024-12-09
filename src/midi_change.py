import usb.core
import usb.util
from JSON import JSON

VENDOR_ID = 0x0483 
PRODUCT_ID = 0x5703 
OUT_ENDPOINT = 0x02

# Find the USB device
device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

if device is None:
    raise ValueError("Device not found")

device.reset()

# Detach kernel driver (if active)
if device.is_kernel_driver_active(0):
    device.detach_kernel_driver(0)

# Set device configuration
device.set_configuration()


effects = JSON.get_json("../effects.json")

# last_effect = "0"
# Listen for outgoing communication and send the selected command
def select_effect():
    while True:
        try:
            effect = input("Enter the effect/name to select an effect ('q' to quit, 'h' for help): ")
            if effect.lower() == 'q':
                print("Exiting...")
                break
            if effect == "": # If press enter, select the next effect
                effect = str(int(last_effect) + 2)
            elif not effect.isdigit() or int(effect) not in range(1, len(effects)):
                print("Invalid input. Please enter a valid effect effect/name.")
                continue

            effect = str(int(effect) - 1) 
            last_effect = effect
            effect_command = effects[effect]
            for _ in range(2): # Send the command twice to respect bInterval of 2ms
                device.write(OUT_ENDPOINT, effect_command)
            print(f"Effect {effect} selected")

        except usb.core.USBError as e:
            print(f"USB Error: {e}")
            break
        except Exception as e:
            print(f"Error: {e}")
            break

# Start the interception loop
select_effect()
