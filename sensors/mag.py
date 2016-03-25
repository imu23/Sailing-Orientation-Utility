## Magnetometer Raw Data Collector
#	 EHH

from Adafruit_I2C import Adafruit_I2C

class Magnetometer(Adafruit_I2C):
	
	# Assign registers
    LSM303_ADDRESS_MAG   = (0x3C >> 1)
    LSM303_REGISTER_MAG_CRB_REG_M     = 0x01
    LSM303_REGISTER_MAG_MR_REG_M      = 0x02
    LSM303_REGISTER_MAG_OUT_X_H_M     = 0x03
    
    # Gain settings for setMagGain()
    LSM303_MAGGAIN_1_3 = 0x20 # +/- 1.3
    LSM303_MAGGAIN_1_9 = 0x40 # +/- 1.9
    LSM303_MAGGAIN_2_5 = 0x60 # +/- 2.5
    LSM303_MAGGAIN_4_0 = 0x80 # +/- 4.0
    LSM303_MAGGAIN_4_7 = 0xA0 # +/- 4.7
    LSM303_MAGGAIN_5_6 = 0xC0 # +/- 5.6
    LSM303_MAGGAIN_8_1 = 0xE0 # +/- 8.1
    
    def __init__(self, busnum=-1, debug=False, hires=False):
		# Create new I2C instance
        self.mag = Adafruit_I2C(self.LSM303_ADDRESS_MAG  , busnum, debug)
		
		# Enable the magnetometer
        self.mag.write8(self.LSM303_REGISTER_MAG_MR_REG_M, 0x00)
        
    # Interpret signed 16-bit magnetometer component from list
    def mag16(self, list, idx):
        n = (list[idx] << 8) | list[idx+1]   # High, low bytes
        return n if n < 32768 else n - 65536 # 2's complement signed
        
    def read(self):
		# Read the magnetometer
        list = self.mag.readList(self.LSM303_REGISTER_MAG_OUT_X_H_M, 6)
        res = [ self.mag16(list, 0),
                    self.mag16(list, 2),
                    self.mag16(list, 4) ]
        return res
                    
    def setMagGain(gain=LSM303_MAGGAIN_1_3):
        self.mag.write8( LSM303_REGISTER_MAG_CRB_REG_M, gain)

if __name__ == '__main__':
	
	from time import sleep
	import os
	from process_compass import getMag
	import accel as ac
	
	mag = Magnetometer()
	accel = ac.Accelerometer()
	timer = 0
	sleeptime = 0.5
	
	while True:
		os.system('clear')
		raw = mag.read()
		m = getMag(accel.read(), raw)
		print raw
		#print m
		
		sleep(sleeptime)
