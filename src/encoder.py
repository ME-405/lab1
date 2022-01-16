''' @file                       encoder.py
    @brief                      A driver for reading from Quadrature Encoders
    @author                     Nick De Simone, Jacob-Bograd, Horacio Albarran
    @date                       January 16, 2022
'''
## Importation of libraries
import pyb

class Encoder:
    ''' @brief                  Interface with quadrature encoders
        @details                Initializes encoder objects and implements 
                                methods to work directly with encoder hardware
    '''

    def __init__(self):
        ''' @brief   Encoder Driver to manipulate physical encoders
            @details Constructs encoder objects by linking specified
                     encoder numbers to corresponding Nucleo pins
            @param   encoder_num Specify Encoder 1 or 2
        '''

        ## Prime Pin B6&7 on PCB to be used as timer objects with Encoder 1
        self.pinB6 = pyb.Pin(pyb.Pin.cpu.B6)
        self.pinB7 = pyb.Pin(pyb.Pin.cpu.B7)

        ## Prime Pin C6&7 on PCB to be used as timer objects with Encoder 2
        self.pinC6 = pyb.Pin(pyb.Pin.cpu.C6)
        self.pinC7 = pyb.Pin(pyb.Pin.cpu.C7)

        ## Reference Count used to compute change in encoder position (delta)
        # ref_count will update in each run through the "update" method
		self.ref_count = 0
		
        ## Current Position: Position in [ticks] of the associated encoder
        # current_pos will update in each run through the "update" method       
        self.current_pos = 0
        self.delta = 0

        ## Establish Period for Encoder Counting, used to correct for overflow
        self.period = 65535 #period in Hz

    def update(self):
        ''' @details			Provides with the current position provided by the chosen encoder
            @return             The position of the encoder shaft
        '''
		# Actualizing the encoder position 
        self.update_count = self.timer.counter()
		
		# Obtaining the difference between the encoder positions
        self.delta = self.update_count - self.ref_count
		
		# Correcting for overflow and underflow of the encoder reader value
        if self.delta > 0 and self.delta > self.period/2:
            self.delta -= self.period
        elif self.delta < 0 and abs(self.delta) > self.period/2:
            self.delta += self.period
		else:
			print('Error in updated delta value')

#        self.ref_count = self.timer.counter()
		# Setting the reference position based on the "current" encoder position
        self.ref_count = self.update_count
		# Updating the current position based on the provided delta value
        self.current_pos += self.delta
     
    def get_position(self):
        ''' @brief      Retrieve encoder position in [ticks]
            @details    Returns encoder position at time of function call
            @return     current_pos
        '''

        return self.current_pos

    def set_position(self, position):
        ''' @brief      Allow user to set position in [ticks] of encoder
            @details    Calls for user to enter a position value for the 
                        associated encoder
            @param  position    The new position of the encoder shaft
        '''
        self.current_pos = position

    def get_delta(self):
        ''' @brief      Return change in encoder position in [ticks]
            @details    Returns change in encoder position between time of 
                        function call and previous encoder update
            @return             The change in position of the encoder shaft
                                between the two most recent updates
        '''
#        self.update_count = self.timer.counter()
#        self.delta = self.update_count - self.ref_count
#        if self.delta > 0 and self.delta > self.period/2:
#            self.delta += self.period
#        if self.delta < 0 and abs(self.delta) > self.period/2:
#            self.delta -= self.period
        #self.update()
        return self.delta
		
	def run(self,encoder_num)
		'''
		@details It creates a function to run the encoder.py file based on the provided encoder that
				 wants to be run
		'''
		## Create class variable according to specified encoder number
        self.encoder_num = encoder_num
		
		# Evaluate specified encoder number (1 or 2)
        # Create timer objects associated with the appropriate encoder        
        if self.encoder_num == 1:
            self.timer = pyb.Timer(4, prescaler = 0, period = self.period)
            ## Link Encoder Channels
            self.t4ch1 = self.timer.channel(1, pyb.Timer.ENC_AB, pin=self.pinB6)
            self.t4ch2 = self.timer.channel(2, pyb.Timer.ENC_AB, pin=self.pinB7)
#            print('Created encoder object associated with Encoder 1')
			
			# Getting the values for the encoder
			self.set_position()
			self.update()
			self.get_position()
			self.get_delta()

        elif self.encoder_num == 2:
            self.timer = pyb.Timer(8, prescaler = 0, period = self.period)
            ## Link Encoder Channels
            self.t8ch1 = self.timer.channel(1, pyb.Timer.ENC_AB, pin=self.pinC6)
            self.t8ch2 = self.timer.channel(2, pyb.Timer.ENC_AB, pin=self.pinC7)
#            print('Created encoder object associated with Encoder 2')

			# Getting the values for the encoder
			self.set_position()
			self.update()
			self.get_position()
			self.get_delta()
			
		else:
			print('Please provide with the encoder that wants to be used')
		
		
