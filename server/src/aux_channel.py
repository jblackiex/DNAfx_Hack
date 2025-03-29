import os
import pygame
from time import sleep
from input_output_channel import InputOutputChannel
from ENV import ENV

class AuxChannel(InputOutputChannel):
    """Implementation of Socket input channel."""

    def send(self, data, aux_data: list) -> None:
        try:

            DIR_TRACKS = ENV.get("DIR_TRACKS")
            data = DIR_TRACKS + data[7:] + ".wav" # data[7:] to remove the prefix "recMODE_"
            if not os.path.exists(data):
                print(f"File '{data}' not found in directory './tracks'.")
                return

            GPIO_PIN_BACK = ENV.get("GPIO_PIN_BACK")
            GPIO_PIN_NEXT = ENV.get("GPIO_PIN_NEXT")
            # Initialize the pygame mixer
            print(f"Loading '{data}'...")

            pygame.mixer.init()
            pygame.mixer.music.load(data)

            sleep(0.5) # finish setting up the audio channel.
            pygame.mixer.music.play()
            os.system(f"sudo gpioget --bias=pull-down gpiochip0 {GPIO_PIN_BACK}") # start recording
            os.system(f"sudo gpioget --bias=pull-up gpiochip0 {GPIO_PIN_BACK}") # start recording
                
                # Wait for the playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(200)
            sleep(0.135) # finish setting up the audio channel.
            os.system(f"sudo gpioget --bias=pull-down gpiochip0 {GPIO_PIN_NEXT}") # stop recording
            os.system(f"sudo gpioget --bias=pull-up gpiochip0 {GPIO_PIN_NEXT}")
            pygame.mixer.quit()
            aux_data[0] = data
        except Exception as e:
            print(f"An error occurred while playing the file: {e}")

    def receive_on(cls, channeldata: list) -> None:
        pass
