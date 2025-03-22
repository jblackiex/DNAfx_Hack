import os
import pygame
from input_output_channel import InputOutputChannel
from ENV import ENV

class AuxChannel(InputOutputChannel):
    """Implementation of Socket input channel."""

    def __init__(self):
        file_name = "./tracks/audiomass-output.mp3"
        
        if not os.path.exists(file_name):
            print(f"File '{file_name}' not found in directory './tracks'.")
            return

        # Analyze the BPM and number of beats before playback
        # print("Analyzing BPM and number of beats...")
        # bpm, num_beats = analyze_bpm(file_path)
        # if bpm:
        #     print(f"Estimated BPM: {bpm}")
        #     print(f"Total number of beats: {num_beats}")
        # else:
        #     print("Unable to estimate BPM or beats.")
        
        # Initialize the pygame mixer
        pygame.mixer.init()
        print(f"Loading '{file_name}'...")
        
        # Load and play the file
        pygame.mixer.music.load(file_name)


    def send(self, preset, last_preset):
        try:
            pygame.mixer.music.play()
                
                # Wait for the playback to finish
            os.system(f"sudo gpioget --bias=pull-down gpiochip0 {ENV.get('GPIO_PIN_BACK')}") # start recording
            os.system(f"sudo gpioget --bias=pull-up gpiochip0 {ENV.get('GPIO_PIN_BACK')}") # start recording
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(120)
            os.system(f"sudo gpioget --bias=pull-down gpiochip0 {ENV.get('GPIO_PIN_NEXT')}") # stop recording
            os.system(f"sudo gpioget --bias=pull-up gpiochip0 {ENV.get('GPIO_PIN_NEXT')}")
        except Exception as e:
            print(f"An error occurred while playing the file: {e}")

    def receive_on(cls, channeldata: list) -> None:
        pass

    def __del__(self):
        pygame.mixer.quit()

