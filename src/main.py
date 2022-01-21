''' @file                       main.py
    @brief                      File that runs the encoder and motor
    @author                     Nick De Simone, Jacob-Bograd, Horacio Albarran
    @date                       January 16, 2022
'''

from Motor import MotorDriver
from encoder import Encoder
from pyb import Pin
import pyb

import time




if __name__ == '__main__':
    # Variable for the encoder1
    encoderPin1 = pyb.Pin(pyb.Pin.cpu.C6)
    encoderPin2 = pyb.Pin(pyb.Pin.cpu.C7)
    EncoderDriver = Encoder(encoderPin1, encoderPin2, 3, 1, 2)
    print("Encoder Done")

    # Variable for the Motor code
    motorEnable = pyb.Pin(pyb.Pin.cpu.A10, pyb.Pin.IN, pyb.Pin.PULL_UP)
    motorPin1 = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
    motorPin2 = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
    motorTimer = pyb.Timer(3, freq=20000)
    Motor = MotorDriver(motorEnable, motorPin1, motorPin2, motorTimer, 1, 2)
    print("Motor Done")
    #EncoderDriver.update()    # Provide with the desired encoder
    #Motor.enable()
    motorEnable.value(False)
    print("JUST ENABLED")
    #time.sleep(.5)
    duty = 100
    Motor.set_duty_cycle(duty)   # Provide with the desired motor and duty_cycle
#     while(True):
# #         try:
#         EncoderDriver.update()
#         print(EncoderDriver.get_position())
#         time.sleep(.1)
#             if(duty < 40):
#                 up = 1
#             elif (duty > 90):
#                 up = 0
#             if(up == 1):
#                 duty += 1
#             else:
#                 duty -= 1
            #Motor.set_duty_cycle(duty)
#         except KeyboardInterrupt:
#             Motor.disable()
#             break