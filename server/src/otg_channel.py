import asyncio
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write, read
import os
from ENV import ENV

class OtgChannel():
    """Implementation of OTG input channel."""
    def __init__(self):
        # Parameters for recording
        self.RATE = 44100  # Sampling rate (Hz)
        self.DURATION = 10  # Duration in seconds
        self.CHANNELS = 2  # Number of audio channels (2 for stereo)
        self.OUTPUT_FILENAME = None

    def export_audio_from_dnafx_looper(self, data: str) -> None:
        try:
            print(f"Recording {self.CHANNELS}-channel audio (stereo)...")
            
            DIR_TRACKS = ENV.get("DIR_TRACKS")
            self.OUTPUT_FILENAME = "./" + DIR_TRACKS + data[11:]
            
            # Find the index of the second underscore
            first_underscore_index = 11
            second_underscore_index = data.find('_', first_underscore_index + 1)

            # Extract the part after the second underscore
            number_part = data[second_underscore_index + 1:]

            try:
                self.DURATION = float(number_part)  # Set the duration based on the extracted number
            except ValueError:
                self.DURATION = 10  # Default duration if conversion fails

            os.system(f"sudo gpioget --bias=pull-down gpiochip0 {ENV.get('GPIO_PIN_BACK')}") # Button left/back dnafx pedal
            os.system(f"sudo gpioget --bias=pull-up gpiochip0 {ENV.get('GPIO_PIN_BACK')}")

            audio_data = sd.rec(int(self.RATE * self.DURATION), samplerate=self.RATE, channels=self.CHANNELS, dtype='int16')
            sd.wait()  # Wait until recording is finished
            print("Recording complete.")
            
            os.system(f"sudo gpioget --bias=pull-down gpiochip0 {ENV.get('GPIO_PIN_NEXT')}") # Button right/next dnafx pedal
            os.system(f"sudo gpioget --bias=pull-up gpiochip0 {ENV.get('GPIO_PIN_NEXT')}")

            # Save as WAV file
            filename = data[11:second_underscore_index]
            write(DIR_TRACKS + filename, self.RATE, audio_data)
            print(f"Audio saved as {self.OUTPUT_FILENAME}")
        except Exception as e:
            print(f"An error occurred while recording audio: {e}")
   