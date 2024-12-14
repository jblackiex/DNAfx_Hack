import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

# Parameters for recording
RATE = 44100  # Sampling rate (Hz)
DURATION = 10  # Duration in seconds
CHANNELS = 2  # Number of audio channels (2 for stereo)
OUTPUT_FILENAME = "audiomass-output.wav"  # Output file name

def record_stereo_audio():
    print(f"Recording {CHANNELS}-channel audio (stereo)...")
    
    # Record audio
    audio_data = sd.rec(int(RATE * DURATION), samplerate=RATE, channels=CHANNELS, dtype='int16')
    sd.wait()  # Wait until recording is finished
    
    print("Recording complete.")
    
    # Save as WAV file
    write(OUTPUT_FILENAME, RATE, audio_data)
    print(f"Audio saved as {OUTPUT_FILENAME}")

if __name__ == "__main__":
    record_stereo_audio()
