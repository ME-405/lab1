''' @file                       main.py
    @brief                      File that runs the encoder and motor
    @author                     Nick De Simone, Jacob-Bograd, Horacio Albarran
    @date                       January 16, 2022
'''

import DRV8847_Motor as MotorDriver
import encoder as Encoder 

# Variable for the encoder
EncoderDriver = Encoder()    

# Variable for the Motor code
Motor = MotorDriver() 


if __name__ = '__main__'
    EncoderDriver.run(1)    # Provide with the desired encoder
    MotorDriver.run(1,70)   # Provide with the desired motor and duty_cycle