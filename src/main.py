'''!
     @file                       main.py
     @brief                      File that runs the encoder and motor
     @author                     Nick De Simone, Jacob-Bograd, Horacio Albarran
     @date                       January 22, 2022
'''

# Importing libraries and classes,
from Motor import MotorDriver
from encoder import Encoder
from pyb import Pin
import pyb
import time

# Instantiated object for the encoder as well as timer,
encoderPin1 = pyb.Pin(pyb.Pin.cpu.C6)
encoderPin2 = pyb.Pin(pyb.Pin.cpu.C7)
EncTimer = 8
EncoderDriver = Encoder(encoderPin1, encoderPin2, EncTimer, 1, 2)

# Instantiated the objects for the chosen Motor,
motorEnable = pyb.Pin(pyb.Pin.cpu.A10, pyb.Pin.IN, pyb.Pin.PULL_UP)
motorPin1 = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
motorPin2 = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
motorTimer = pyb.Timer(3, freq=20000)                     
Motor = MotorDriver(motorEnable, motorPin1, motorPin2, motorTimer, 1, 2)


if __name__ == '__main__':
    Motor.enable()               # Enables motor
    up = 0                       # Counts up while looping in ordert to reset to a value position of zero
    duty = 30                    # Setting the duty cycle initiallly to 70%
                                 #     Minimum duty cycle of motor was found to be 30% and highest 100%
    Motor.set_duty_cycle(duty)   # Setting the duty cycle on motors
    
    while(True):
        try:
            EncoderDriver.update()      # Updating duty cycle reading
            time.sleep(.1)              # Sleeping for 0.1 sec before getting an update from the encoder position
            up += 2                     # Counting for initiation of encoder position
            if up > 100:
                up = 0
                EncoderDriver.zero()
            else:
                pass
            
        except KeyboardInterrupt:
            Motor.disable()
            break
    print('out of loop')
        


            
