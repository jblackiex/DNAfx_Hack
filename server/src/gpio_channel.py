from output_channel import OutputChannel
from aux_channel import AuxChannel
from otg_channel import OtgChannel
from ENV import ENV
import os
from time import sleep

class GPIOChannel(OutputChannel):
    """Implementation of GPIO output channel."""
    def __init__(self):
        self.aux_channel = AuxChannel()
        self.otg_channel = OtgChannel()

    def send(self, data: str, aux_data: list) -> None:
        if (ENV.get("USE_GPIO") == "ON"):
            if (data == "recMODE"):
                # now we upload the track and send it via AUX with a time that allows us to stop the recording via GPIO 
                print(f"Sending via GPIO: recMODE")
                self.aux_channel.send(data, aux_data) # send the track (aux_data) to the aux channel OR reproduce the track via AUX
                print(f"[Looper] Aux data imported: {aux_data}")
            elif (data == "playMODE"): # play recording if already exists or play/dub the track
                print(f"Sending via GPIO: playMODE")
                os.system(f"sudo gpioget --bias=pull-down gpiochip0 {ENV.get('GPIO_PIN_BACK')}") # Button left/back dnafx pedal
                os.system(f"sudo gpioget --bias=pull-up gpiochip0 {ENV.get('GPIO_PIN_BACK')}")
                print(f"[Looper] playMODE")
            elif (data == "stopMODE"): # stop recording
                print(f"Sending via GPIO: stopMODE")
                os.system(f"sudo gpioget --bias=pull-down gpiochip0 {ENV.get('GPIO_PIN_NEXT')}") # Button right/next dnafx pedal
                os.system(f"sudo gpioget --bias=pull-up gpiochip0 {ENV.get('GPIO_PIN_NEXT')}")
                print(f"[Looper] stopMODE")
            elif (data == "looperMODE"): # access to looper mode or clear recording
                print(f"Sending via GPIO: looperMODE")
                os.system(f"sudo gpioget --bias=pull-down gpiochip0 {ENV.get('GPIO_PIN_NEXT')}") # Button right/next dnafx pedal
                sleep(1)
                os.system(f"sudo gpioget --bias=pull-up gpiochip0 {ENV.get('GPIO_PIN_NEXT')}")
                print(f"[Looper] looperMODE")
            elif (data == "otgMODE"):
                self.otg_channel.import_stereo_audio()
            elif (data == "tunerMODE"): # access to tuner mode
                print(f"Sending via GPIO: tunerMODE")
                os.system(f"sudo gpioget --bias=pull-down gpiochip0 {ENV.get('GPIO_PIN_BACK')}") # Button left/back dnafx pedal
                sleep(1)
                os.system(f"sudo gpioget --bias=pull-up gpiochip0 {ENV.get('GPIO_PIN_BACK')}")
                print(f"[Tuner] activated")