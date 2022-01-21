'''
@file  DRV8847_Motor.py
@brief A container for the interaction for the physical equipment 
@author: Nick De Simone, Jacob-Bograd, Horacio Albarran
@date	January 16, 2022
'''

## Importation of libraries
import pyb
from pyb import Pin
from pyb import ExtInt
import time

class MotorDriver:
    
    def __init__(self, en_pin, in1pin, in2pin, inputTimer, channel1, channel2):
        '''
        @brief It will initialize the variables on the main file as well as motor defaults; MotorDriver-Class.
        '''
        # Initialize Motor 1 pins to be handled as PWM objects
        self.Pin1 = in1pin
        self.Pin2 = in2pin
        # Define motor timer frequency. Must be >20kHz to avoid noise
        self.timer = inputTimer
        # Initialize the board's nSLEEP pin to be enabled and disabled
        self.enable = en_pin
        self.ch1 = self.timer.channel(channel1, pyb.Timer.PWM, pin=self.Pin1)
        self.ch2 = self.timer.channel(channel2, pyb.Timer.PWM, pin=self.Pin2)
        self.pinB2 = pyb.Pin(pyb.Pin.cpu.B2)
        self.faultInt = pyb.ExtInt(self.pinB2, mode=pyb.ExtInt.IRQ_FALLING, pull=pyb.Pin.PULL_NONE, callback=self.fault_cb)
        print("DEBUG: PIN1 ", self.Pin1, "\n PIN2", self.Pin2, "\n enPIN", self.enable)
        self.enable.value(True)
        print("DEBUG: ENABLED")
              

        
    def enable(self):
        '''
        @brief Enable the motor
        '''
        print("DEBUG: GOING TO ENABLE")
        self.enable.value(True)
        print("DEBUG: ENABLED")
        

    
    def disable(self):
        '''
        @brief Disable the motor
        '''
        self.enable.value(False)
        
        
    def set_duty_cycle(self, duty):
        '''
        @details Setting duty performance for the motor
        '''
        if duty >= 0:
            self.ch1.pulse_width_percent(duty)
            self.ch2.pulse_width_percent(0)
            print('Setting duty cycle to ' + str(duty))

        else:
            self.ch1.pulse_width_percent(0)
            self.ch2.pulse_width_percent(-duty)
            print('Setting duty cycle to NEGATIVE' + str(duty))
        print("DUTY CYCLE SET")

    def fault_cb(self, IRQ_src):
        '''
        @brief It will report if there is any errors detected within the operation of the system
        '''
        while(True):
            print('Motor fault detected')
            print('Disabling motor')
        #self.disable()
    

# class Motor:
# '''
# @details Implementation of the motor driver 
# '''
#     
#     def __init__(self, ch1, ch2):
# 		'''
# 		@details Initializing the implementation of the motor driver and parameters
# 		'''
# 		
# 		# Setting channels
#         self.channel_1 = ch1
#         self.channel_2 = ch2
#         
#     
#             
    def clear_fault(self):
        '''
        @details Enabling motor to perform as well as receiving signals from the control panel
        '''
        self.enable()      

# 	def run(self,motorNumber,duty_val)
# 		'''
# 		@details It allows to run the motor file from a main.py document
# 		'''
# 		DRV8847.motor(motorNumber)
# 		DRV8847.enable()
# 		self.set_duty(duty_val)
# 		
# 		