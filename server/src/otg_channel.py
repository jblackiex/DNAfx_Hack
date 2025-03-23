from input_channel import InputChannel
import asyncio
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

class OtgChannel(InputChannel):
    """Implementation of OTG input channel."""
    def __init__(self):
        # Parameters for recording
        self.RATE = 44100  # Sampling rate (Hz)
        self.DURATION = 10  # Duration in seconds
        self.CHANNELS = 2  # Number of audio channels (2 for stereo)
        self.OUTPUT_FILENAME = "audiomass-output.wav"  # Output file name

    def record_stereo_audio(self):
        print(f"Recording {self.CHANNELS}-channel audio (stereo)...")
        
        # Record audio
        audio_data = sd.rec(int(self.RATE * self.DURATION), samplerate=self.RATE, channels=self.CHANNELS, dtype='int16')
        sd.wait()  # Wait until recording is finished
        
        print("Recording complete.")
        
        # Save as WAV file
        write(self.OUTPUT_FILENAME, self.RATE, audio_data)
        print(f"Audio saved as {self.OUTPUT_FILENAME}")

    async def receive_on(cls, channeldata: list, event_data_received: asyncio.Event = None) -> None:
        pass