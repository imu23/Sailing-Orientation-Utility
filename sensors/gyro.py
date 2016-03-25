## Gyroscope Raw Data Collector

from Adafruit_I2C import Adafruit_I2C

class Gyroscope(Adafruit_I2C):
	# Assign registers
    L3GD20_ADDRESS       = (0xD6 >> 1)
    L3GD20_REGISTER_CTRL_REG1_A       = 0x20
    L3GD20_REGISTER_CTRL_REG4_A       = 0x23
    L3GD20_REGISTER_GYRO_OUT_X_L      = 0x28
    
    def __init__(self, busnum=-1, debug=False, hires=False):
		# Create new I2C instance
        self.gyro  = Adafruit_I2C(self.L3GD20_ADDRESS      , busnum, debug)
		
		# Enable the gyroscope
        self.gyro.write8(self.L3GD20_REGISTER_CTRL_REG1_A, 0x0F)
        self.gyro.write8(self.L3GD20_REGISTER_CTRL_REG4_A, 0x30)
        
    # Interpret signed 16-bit gyroscope component from list
    def gyro16(self, list, idx):
        n = (list[idx+1] << 8) | list[idx]   # Low,high bytes
        return n if n < 32768 else n - 65536 # 2's complement signed
    
    # Read the gyroscope
    def read(self):
        list = self.gyro.readList(self.L3GD20_REGISTER_GYRO_OUT_X_L | 0x80, 6)
        res = [self.gyro16(list, 0),
                   self.gyro16(list, 2),
                   self.gyro16(list, 4)]
        return res

if __name__ == '__main__':
	
	from time import sleep
	import os
	
	gyro = Gyroscope()
	timer = 0
	sleeptime = 0.5
	
	while True:
		os.system('clear')
		g = gyro.read()
		print g
		sleep(sleeptime)
