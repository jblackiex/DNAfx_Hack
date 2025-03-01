import librosa
import numpy as np
from pydub import AudioSegment

def extract_and_save_loop(input_file, output_file="extracted_loop.wav"):
    """
    Detects a repeating loop in an audio file and saves the extracted loop.

    Args:
        input_file (str): Path to the input audio file.
        output_file (str): Path to save the extracted loop (default: 'extracted_loop.wav').

    Returns:
        None
    """
    try:
        # Load the audio file
        y, sr = librosa.load(input_file, sr=None)
        
        # Compute chroma features
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        
        # Compute the self-similarity matrix
        similarity_matrix = librosa.segment.recurrence_matrix(chroma, mode='affinity', self=False)

        # Find the most similar repeating segments
        similarity_sum = similarity_matrix.sum(axis=0)
        loop_start_idx = np.argmax(similarity_sum)
        loop_end_idx = loop_start_idx + int(sr * 3 / librosa.frames_to_samples(1))  # Assume a 3-second loop

        # Convert frame indices to time
        start_time = librosa.frames_to_time(loop_start_idx, sr=sr)
        end_time = librosa.frames_to_time(loop_end_idx, sr=sr)

        print(f"Detected loop from {start_time:.2f}s to {end_time:.2f}s")

        # Convert time to milliseconds for pydub
        start_ms = int(start_time * 1000)
        end_ms = int(end_time * 1000)

        # Load the audio file using pydub and extract the loop
        audio = AudioSegment.from_file(input_file)
        loop = audio[start_ms:end_ms]

        # Save the extracted loop
        loop.export(output_file, format="wav")
        print(f"Extracted loop saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example Usage
input_file = "output_audio_u.wav"  # Replace with your input audio file
extract_and_save_loop(input_file)