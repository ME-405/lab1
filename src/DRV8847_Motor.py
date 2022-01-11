import pyb
from pyb import Pin
from pyb import ExtInt
import time

class DRV8847:
    
    def __init__(self):
        
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
        self.faultInt.disable()
        self.pinA15.value(True)
        time.sleep(.025)
        self.faultInt.enable()
    
    def disable(self):
        self.pinA15.value(False)
    
    def fault_cb(self, IRQ_src):
        print('Motor fault detected')
        print('Disabling motor')
        self.disable()
    
    def motor(self, motorNum=1):
        if motorNum == 1:
            t3ch1 = self.tim3.channel(1, pyb.Timer.PWM, pin=self.pinB4)
            t3ch2 = self.tim3.channel(2, pyb.Timer.PWM, pin=self.pinB5)
            return Motor(t3ch1, t3ch2)
        else:
            t3ch3 = self.tim3.channel(3, pyb.Timer.PWM, pin=self.pinB0)
            t3ch4 = self.tim3.channel(4, pyb.Timer.PWM, pin=self.pinB1)
            return Motor(t3ch3, t3ch4)

class Motor:
    
    def __init__(self, ch1, ch2):
        self.channel_1 = ch1
        self.channel_2 = ch2
        
    
    def set_duty(self, duty):
        if duty >= 0:
            self.channel_1.pulse_width_percent(duty)
            self.channel_2.pulse_width_percent(0)
        else:
            self.channel_1.pulse_width_percent(0)
            self.channel_2.pulse_width_percent(-duty)
            
    def clear_fault(self):
        DRV8847.enable()        