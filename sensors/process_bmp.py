## Processing BMP180 Data

from Adafruit_I2C import Adafruit_I2C

class bmp_processor(object):
	# BMP180 Registers
	BMP180_CAL_AC1           = 0xAA  # R   Calibration data (16 bits)
	BMP180_CAL_AC2           = 0xAC  # R   Calibration data (16 bits)
	BMP180_CAL_AC3           = 0xAE  # R   Calibration data (16 bits)   
	BMP180_CAL_AC4           = 0xB0  # R   Calibration data (16 bits)
	BMP180_CAL_AC5           = 0xB2  # R   Calibration data (16 bits)
	BMP180_CAL_AC6           = 0xB4  # R   Calibration data (16 bits)
	BMP180_CAL_B1            = 0xB6  # R   Calibration data (16 bits)
	BMP180_CAL_B2            = 0xB8  # R   Calibration data (16 bits)
	BMP180_CAL_MB            = 0xBA  # R   Calibration data (16 bits)
	BMP180_CAL_MC            = 0xBC  # R   Calibration data (16 bits)
	BMP180_CAL_MD            = 0xBE  # R   Calibration data (16 bits)

	# constants
	ac1 = 408
	ac2 = -72
	ac3 = -14383
	ac4 = 32741
	ac5 = 32757
	ac6 = 23151
	b1 = 6190
	b2 = 4
	mb = -32767
	mc = -8711
	md = 2868

    # Calibrate the sensor. Just do this once per use
	def calibrate(self, device):
	
		self.ac1 = device.readS16(self.BMP180_CAL_AC1, False)
		self.ac2 = device.readS16(self.BMP180_CAL_AC2, False)
		self.ac3 = device.readS16(self.BMP180_CAL_AC3, False)
		self.ac4 = device.readU16(self.BMP180_CAL_AC4, False)
		self.ac5 = device.readU16(self.BMP180_CAL_AC5, False)
		self.ac6 = device.readU16(self.BMP180_CAL_AC6, False)
		self.b1 = device.readS16(self.BMP180_CAL_B1, False)
		self.b2 = device.readS16(self.BMP180_CAL_B2, False)
		self.mb = device.readS16(self.BMP180_CAL_MB, False)
		self.mc = device.readS16(self.BMP180_CAL_MC, False)
		self.md = device.readS16(self.BMP180_CAL_MD, False)
		
	# Helper to get the B5 variable
	def getB5(self, raw_temp):
        # bit manipulation
		
		X1 = (int(raw_temp - self.ac6) * self.ac5) >> 15
		X2 = (self.mc << 11) / (X1 + self.md)
		B5 = X1 + X2
		return B5
    
    # process the raw temperature data
	def procTemp(self, raw_temp):
		B5 = self.getB5(raw_temp)
		temp = ((B5 + 8) >> 4) / 10.0
		return temp
		
	# process the raw pressure data
	#	note that it needs the temperature data too
	def procPress(self, raw_press, raw_temp):
		# bit manipulation
		mode = 1
		B5 = self.getB5(raw_temp)
		B6 = B5 - 4000
		X1 = (self.b2 * (B6 * B6) >> 12) >> 11
		X2 = (self.ac2 * B6) >> 11
		X3 = X1 + X2
		# assume mode = 1
		B3 = (((self.ac1 * 4 + X3) << mode) + 2) / 4
		X1 = (self.ac3 * B6) >> 13
		X2 = (self.b1 * ((B6 * B6) >> 12)) >> 16
		X3 = ((X1 + X2) + 2) >> 2
		B4 = (self.ac4 * (X3 + 32768)) >> 15
		# assume mode = 1
		B7 = (raw_press - B3) * (50000 >> mode)
		if B7 < 0x80000000:
			p = (B7 * 2) / B4
		else:
			p = (B7 / B4) * 2
		X1 = (p >> 8) * (p >> 8)
		X1 = (X1 * 3038) >> 16
		X2 = (-7357 * p) >> 16
		p = p + ((X1 + X2 + 3791) >> 4)
		return p
		
    
if __name__ == '__main__':
	import press
	import temp
	
	from time import sleep
	from os import system
	
	b = bmp_processor()
	
	
	pr = press.Pressure()
	te = temp.Temperature()
	
	b.calibrate(pr.press)
	sleeptime = 0.5
	
	print dir()
	import sys
	print sys.path
	while True:
		system('clear')
		print b.procTemp(te.read())
		print b.procPress(pr.read(),te.read())
		sleep(sleeptime)

