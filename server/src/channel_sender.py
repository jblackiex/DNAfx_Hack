from usbhid_channel import USBHIDChannel
from gpio_channel import GPIOChannel
from JSON import JSON
from ENV import ENV
class ChannelSender:
    def __init__(self):
        self.last_preset = "0"
        self.channels = {
            "USBHID": USBHIDChannel(),
            "GPIO": GPIOChannel()
        }

    async def send_to(self, channel: str, data: str) -> None:
        try:
            presets = JSON.get_json(ENV.get("DIR_CONFIG") + "/presets.json")
            if data == "": # If press enter, select the next data
                if int(self.last_preset) > 200:
                    self.last_preset = "0"
                data = str(int(self.last_preset) + 2)
            elif not data.isdigit() and data.upper() not in presets:
                if len(data) >= 8 and data[-7:] == f"_add{data[:-3]}":
                    print(f"Adding new preset {data[:-5]} at pos. n. {data[-1:]}")
                    presets.update({data[:-7].upper(): presets[str(int(data[:-3]) - 1)]})
                    JSON.set_json(presets)
            elif not data.isdigit() and data.upper() in presets:
                self.channels[channel].send(data.upper(), presets[data.upper()])
            elif not data.isdigit() or int(data) not in range(1, len(presets)):
                print("Invalid input. Please enter a valid effect index/name.")
                return
            data = str(int(data) - 1)
            effect_command = presets[data]
            self.channels["USBHID"].send(effect_command, data.upper())
            self.last_preset = data
        except Exception as e:
            print(f"Error: {e}")
            raise(f"Error: {e}")