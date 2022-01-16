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

class DRV8847:
    
    def __init__(self):
		'''
        @brief It will initialize the variables on the main file as well as motor defaults; MotorDriver-Class.
        '''
        
        # Initialize Motor 1 pins to be handled as PWM objects
        self.pinB4 = pyb.Pin(pyb.Pin.cpu.B4)
        self.pinB5 = pyb.Pin(pyb.Pin.cpu.B5)
        
        # Initialize Motor 2 pins to be handled as PWM objects
        self.pinB0 = pyb.Pin(pyb.Pin.cpu.B0)
        self.pinB1 = pyb.Pin(pyb.Pin.cpu.B1)
        
        # Initialize the board's nSLEEP pin to be enabled and disabled
        self.pinA15 = pyb.Pin(pyb.Pin.cpu.A15, Pin.OUT_PP)
        
        # Initialize board's nFAULT pin to disable motor when motor faults
        self.pinB2 = pyb.Pin(pyb.Pin.cpu.B2)
        self.faultInt = pyb.ExtInt(self.pinB2, mode=pyb.ExtInt.IRQ_FALLING, 
                                   pull=pyb.Pin.PULL_NONE, callback=self.fault_cb)
        
        # Define motor timer frequency. Must be >20kHz to avoid noise
        self.tim3 = pyb.Timer(3, freq = 20000)
        
    def enable(self):
		'''
        @brief It defines the varible of nSLEEP as high so the motors can function
        '''
        self.faultInt.disable()
        self.pinA15.value(True)
        time.sleep(.025)
        self.faultInt.enable()
    
    def disable(self):
		'''
        @brief It defines the variable of nSLEEP as low so no signal can make the motors function
        '''
        self.pinA15.value(False)
    
    def fault_cb(self, IRQ_src):
		'''
        @brief It will report if there is any errors detected within the operation of the system
        '''
        print('Motor fault detected')
        print('Disabling motor')
        self.disable()
    
    def motor(self, motorNum=1):
		'''
		@brief Setting the operation of the motor with its respective pins and operating channels
		'''
        if motorNum == 1:
            t3ch1 = self.tim3.channel(1, pyb.Timer.PWM, pin=self.pinB4)
            t3ch2 = self.tim3.channel(2, pyb.Timer.PWM, pin=self.pinB5)
            return Motor(t3ch1, t3ch2)
        else:
            t3ch3 = self.tim3.channel(3, pyb.Timer.PWM, pin=self.pinB0)
            t3ch4 = self.tim3.channel(4, pyb.Timer.PWM, pin=self.pinB1)
            return Motor(t3ch3, t3ch4)

class Motor:
'''
@details Implementation of the motor driver 
'''
    
    def __init__(self, ch1, ch2):
		'''
		@details Initializing the implementation of the motor driver and parameters
		'''
		
        self.channel_1 = ch1
        self.channel_2 = ch2
        
    
    def set_duty(self, duty):
		'''
		@details Setting duty performance for the motor
		'''
        if duty >= 0:
            self.channel_1.pulse_width_percent(duty)
            self.channel_2.pulse_width_percent(0)
			print('Setting duty cycle to ' + str(duty))
        else:
            self.channel_1.pulse_width_percent(0)
            self.channel_2.pulse_width_percent(-duty)
			print('Setting duty cycle to ' + str(duty))
            
    def clear_fault(self):
		'''
		@details Enabling motor to perform as well as receiving signals from the control panel
		'''
        DRV8847.enable()      

	def run(self,motorNumber,duty_val)
		'''
		@details It allows to run the motor file from a main.py document
		'''
		DRV8847.motor(motorNumber)
		DRV8847.enable()
		self.set_duty(duty_val)
		
		