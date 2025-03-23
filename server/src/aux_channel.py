import os
import pygame
from time import sleep
from input_output_channel import InputOutputChannel
from ENV import ENV

class AuxChannel(InputOutputChannel):
    """Implementation of Socket input channel."""

    def __init__(self):
        self.file_name = "./tracks/audiomass-output.mp3"
        
        if not os.path.exists(self.file_name):
            print(f"File '{self.file_name}' not found in directory './tracks'.")
            return

    def send(self, preset, last_preset):
        try:
            if self.file_name == None:
                print(f"File '{self.file_name}' not found in directory './tracks'.")
                return
    
            # Initialize the pygame mixer
            print(f"Loading '{self.file_name}'...")

            pygame.mixer.init()
            pygame.mixer.music.load(self.file_name)

            sleep(0.5) # finish setting up the audio channel.
            pygame.mixer.music.play()
            os.system(f"sudo gpioget --bias=pull-down gpiochip0 {ENV.get('GPIO_PIN_BACK')}") # start recording
            os.system(f"sudo gpioget --bias=pull-up gpiochip0 {ENV.get('GPIO_PIN_BACK')}") # start recording
                
                # Wait for the playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(200)
            sleep(0.133)
            os.system(f"sudo gpioget --bias=pull-down gpiochip0 {ENV.get('GPIO_PIN_NEXT')}") # stop recording
            os.system(f"sudo gpioget --bias=pull-up gpiochip0 {ENV.get('GPIO_PIN_NEXT')}")
            pygame.mixer.quit()
        except Exception as e:
            print(f"An error occurred while playing the file: {e}")

    def receive_on(cls, channeldata: list) -> None:
        pass
