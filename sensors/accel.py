## Accelerometer Raw Data Collector

from Adafruit_I2C import Adafruit_I2C

class Accelerometer(Adafruit_I2C):
	
	# Set registers
    LSM303_ADDRESS_ACCEL = (0x32 >> 1)
    LSM303_REGISTER_ACCEL_CTRL_REG1_A = 0x20
    LSM303_REGISTER_ACCEL_CTRL_REG4_A = 0x23 
    LSM303_REGISTER_ACCEL_OUT_X_L_A   = 0x28
    
    def __init__(self, busnum=-1, debug=False, hires=False):
		# New I2C instance
        self.accel = Adafruit_I2C(self.LSM303_ADDRESS_ACCEL, busnum, debug)
		
		# Enable the accelerometer
        self.accel.write8(self.LSM303_REGISTER_ACCEL_CTRL_REG1_A, 0x27)
        # Select hi-res (12-bit) or low-res (10-bit) output mode.
        # Low-res mode uses less power and sustains a higher update rate,
        # output is padded to compatible 12-bit units.
        if hires:
            self.accel.write8(self.LSM303_REGISTER_ACCEL_CTRL_REG4_A,
              0b00001000)
        else:
            self.accel.write8(self.LSM303_REGISTER_ACCEL_CTRL_REG4_A, 0)
            
        # Interpret signed 12-bit acceleration component from list
    def accel12(self, list, idx):
        n = list[idx] | (list[idx+1] << 8) # Low, high bytes
        if n > 32767: n -= 65536           # 2's complement signed
        return n >> 4                      # 12-bit resolution

    def read(self):
        # Read the accelerometer
        res = [0, 0, 0]
        list = self.accel.readList(
          self.LSM303_REGISTER_ACCEL_OUT_X_L_A | 0x80, 6)
        res = [ self.accel12(list, 0),
                 self.accel12(list, 2),
                 self.accel12(list, 4) ]
        return res


if __name__ == '__main__':
	
	from time import sleep
	import os
	
	accel = Accelerometer()
	timer = 0
	sleeptime = 0.5
	
	while True:
		os.system('clear')
		a = accel.read()
		print a
		sleep(sleeptime)
		
