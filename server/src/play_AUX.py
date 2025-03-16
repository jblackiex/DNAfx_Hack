import os
import pygame
import librosa

def analyze_bpm(file_path):
    """
    Analyzes the BPM (tempo) of an audio file using librosa and counts the number of beats.

    Args:
        file_path (str): Path to the audio file.

    Returns:
        tuple: Estimated BPM and the total number of beats.
    """
    try:
        # Load the audio file
        y, sr = librosa.load(file_path, sr=None)
        
        # Estimate the tempo (BPM) and beat frames
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

        # Calculate the number of beats
        num_beats = len(beat_frames)
        
        return tempo, num_beats
    except Exception as e:
        print(f"An error occurred during BPM analysis: {e}")
        return None, None

def play_wav_file(directory, file_name="../audiomass-output.mp3"):
    """
    Plays a .wav file from the specified directory using pygame and analyzes its BPM.

    Args:
        directory (str): Path to the directory containing the .wav file.
        file_name (str): Name of the .wav file (default: 'audiomass-output.wav').
    """
    file_path = os.path.join(directory, file_name)
    
    if not os.path.exists(file_path):
        print(f"File '{file_name}' not found in directory '{directory}'.")
        return

    # Analyze the BPM and number of beats before playback
    print("Analyzing BPM and number of beats...")
    bpm, num_beats = analyze_bpm(file_path)
    if bpm:
        print(f"Estimated BPM: {bpm}")
        print(f"Total number of beats: {num_beats}")
    else:
        print("Unable to estimate BPM or beats.")
    
    try:
        # Initialize the pygame mixer
        pygame.mixer.init()
        print(f"Loading '{file_path}'...")
        
        # Load and play the file
        pygame.mixer.music.load(file_path)
        input("Press Enter to start playback.")
        pygame.mixer.music.play()
        
        # Wait for the playback to finish
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        print("Playback finished.")
    except Exception as e:
        print(f"An error occurred while playing the file: {e}")
    finally:
        pygame.mixer.quit()

# Usage
directory = "./"  # Replace with the path to your directory
play_wav_file(directory)
