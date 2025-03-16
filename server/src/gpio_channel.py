from output_channel import OutputChannel
from ENV import ENV
import os
from time import sleep

class GPIOChannel(OutputChannel):
    """Implementation of GPIO output channel."""
    def __init__(self):
        self.looperMODE = False

    def send(self, data: str, last_preset: list) -> None:
        if (ENV.get("USE_GPIO") == "ON"):
            if (self.looperMODE):
                if (data == "recMODE"):
                    # now we upload the track and send it via AUX with a time that allows us to stop the recording via GPIO 
                    print(f"Sending via GPIO: recMODE")
                    os.system(f"sudo gpioget --bias=pull-down gpiochip0 {ENV.get('GPIO_NEXT')}")
                    os.system(f"sudo gpioget --bias=pull-up gpiochip0 {ENV.get('GPIO_NEXT')}")
            elif (data == "looperMODE"):
                self.looperMODE = True
                print(f"Sending via GPIO: looperMODE")
                os.system(f"sudo gpioget --bias=pull-down gpiochip0 {ENV.get('GPIO_NEXT')}") # Button right/next dnafx pedal
                sleep(0.5)
                os.system(f"sudo gpioget --bias=pull-up gpiochip0 {ENV.get('GPIO_NEXT')}")
            elif (data == "tunerMODE"):
                self.looperMODE = False
                print(f"Sending via GPIO: tunerMODE")
                os.system(f"sudo gpioget --bias=pull-down gpiochip0 {ENV.get('GPIO_PIN_BACK')}") # Button left/back dnafx pedal
                sleep(1)
                os.system(f"sudo gpioget --bias=pull-up gpiochip0 {ENV.get('GPIO_PIN_BACK')}")
