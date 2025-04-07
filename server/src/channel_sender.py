from usbhid_channel import USBHIDChannel
from gpio_channel import GPIOChannel
from JSON import JSON
from ENV import ENV
class ChannelSender:
    def __init__(self):
        self.last_preset = ["-1"]
        self.channels = {
            "USBHID": USBHIDChannel(),
            "GPIO": GPIOChannel()
        }

    async def send_to(self, channel: str, data: str) -> None:
        try:
            if data.strip().startswith("help"):
                parts = data.strip().split(" ")
                command = parts[1] if len(parts) > 1 else ""  # "" mostra tutti i comandi
                print(self.command_help(command))
                return
            self.channels[channel].send(data, self.last_preset)
            print("Enter a command(name/index) to send: ")
        except Exception as e:
            print(f"Error: {e}")
            raise(f"Error: {e}")
    
    def command_help(self, command):
        """
        Provides a description of the specified command.

        Parameters:
        - command (str): The name of the command to describe.

        Returns:
        - str: Description of the command.

        if command is empty, it will print the list of all commands
        """

        # Dictionary to hold command descriptions
        command_descriptions = {
            "''": "Moves to the next preset. If the last preset is 199, it resets to 0.",
            "-": "Moves to the previous preset. If at 0, wraps around to 200.",
            "preset_add_number": (
                "Adds a new preset with the specified name at the given position. "
                "For example, 'CoolEffect_add150' copies the value of preset 150 "
                "HOW IT WORKS: CoolEffect_add_15 add a 'CoolEffect' preset at position 14 "
            ),
            "preset_name": (
                "Sends a preset by name if it exists in the list. For example, 'FLANGER' "
                "HOW IT WORKS: 'FLANGER' preset and activates it."
            ),
            "preset_index": (
                "Sends a preset by its numerical index. Must be within the valid range. "
                "HOW IT WORKS: '15' activates the preset stored at index 14."
            ),
            "looperMODE": (
                "Activates Looper Mode or clears the current recording. This allows you "
                "to start a new looping session from scratch."
            ),
            "auxrecMODE": (
                "In Looper Mode, starts recording, sends the specified audio file via AUX, "
                "then stops recording. For example, 'auxrecMODE_rec1.wav' records the 'rec1.wav' "
                "file into the looper. The track will be available at './tracks/rec1.wav'."
                "HOW IT WORKS: auxrecMODE_file.wav → import on dnafx track ./tracks/track.wav."
            ),
            "tunerMODE": "Activates Tuner Mode, enabling you to tune your instrument.",
            "playMODE": (
                "In Looper Mode, plays the audio or starts recording if the track is empty. "
                "If a track is playing and this command is used again, it will start overdubbing "
                "on the current track. Outside of Looper Mode, it moves to the previous preset."
            ),
            "stopMODE": (
                "In Looper Mode, stops the audio if it's currently playing. Outside of Looper Mode, "
                "it moves to the next preset."
            ),
            "otgexpMODE": (
                "In Looper Mode, plays the audio and uses an OTG cable to export it. Ensure that "
                "an OTG cable is connected for this function to work properly."
                "HOW IT WORKS: otgexpMODE_newrec.wav_3 → create a new track ./tracks/newrec.wav 3 seconds long."
            ),
        }

        if command == "":
            return "\n\n".join(
            f">>>{cmd}<<<:\n~~{desc}" for cmd, desc in command_descriptions.items()
        )

        if command in command_descriptions:
            return f">>>{command}<<<:\n~~{command_descriptions[command]}"
        else:
            return f"???{command}???:\nCommand not found. Please enter a valid command."