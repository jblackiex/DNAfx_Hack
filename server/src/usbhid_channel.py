import usb.core
import usb.util
from output_channel import OutputChannel
from ENV import ENV
from JSON import JSON

class USBHIDChannel(OutputChannel):
    """Implementation of USB HID output channel."""

    def __init__(self):
        # Find the USB self.device using vendor and product IDs from the environment variables
        self.device = usb.core.find(idVendor=ENV.get("VENDOR_ID"), idProduct=ENV.get("PRODUCT_ID"))

        if self.device is None:
            raise ValueError(f"{self.device} not found")

        # Reset the self.device to ensure it starts in a clean state
        # This is useful for reinitializing the self.device in case it was previously in use
        self.device.reset()

        # If the self.device is currently controlled by the OS kernel, detach it
        # This allows our script to take direct control of the USB self.device
        if self.device.is_kernel_driver_active(0):
            self.device.detach_kernel_driver(0)

        # Configure the USB self.device with its default settings
        # This sets up endpoints, interfaces, and other communication parameters
        # Necessary before any communication can occur
        self.device.set_configuration()
        print(f"USBHID device: {hex(ENV.get('VENDOR_ID'))}:{hex(ENV.get('PRODUCT_ID'))} found")

    def send(self, data: str, last_preset: list) -> None:
        try:
            if ("MODE" not in data.upper()):
                presets = JSON.get_json(ENV.get("DIR_CONFIG") + "presets.json")
                if data == "":
                    print("Moving to next preset")
                    if int(last_preset[0]) >= 199:
                        self.device.reset()
                        last_preset[0] = 0
                    data = str(int(last_preset[0]) + 2)
                elif data == "-":
                    print("Moving to previous preset")
                    if  0 <= int(last_preset[0]) < 1:
                        last_preset[0] = "200"
                    data = str(int(last_preset[0]))
                elif not data.isdigit() and data.upper() not in presets:
                    if len(data) >= 8 and data[-7:] == f"_add{data[-3:]}":
                        print(f"Adding new preset {data[:-7]} at pos. n. {data[-3:]}")
                        presets.update({data[:-7].upper(): presets[str(int(data[-3:]) - 1)]})
                        JSON.set_json(presets, ENV.get("DIR_CONFIG") + "presets.json")
                        last_preset[0] = str(int(data[-3:]) - 1)
                        return
                elif not data.isdigit() and data.upper() in presets: # "zero" instead of "0" example
                    # SEND PRESET
                    self.send_to_dnafx(presets[data.upper()], data)
                    return
                elif not data.isdigit() or int(data) not in range(1, len(presets)):
                    print("Invalid input. Please enter a valid effect index/name.")
                    return
                
                data = str(int(data) - 1)
                preset_command = presets[data]
                last_preset[0] = data
                
                # SEND PRESET
                self.send_to_dnafx(preset_command, data)
        except usb.core.USBError as e:
            print(f"USB Error: {e}")
            self.device.reset()
            # raise ValueError(f"USB Error: {e}")
        except Exception as e:
            print(f"An error occurred while sending data: {e}")


    def send_to_dnafx(self, preset_command: str, data) -> None:
        for _ in range(2): # Send the command twice to respect bInterval of 2ms
            self.device.write(ENV.get("OUT_ENDPOINT"), preset_command)

        print(f"Successfully sent via USBHID: {data.upper()}")