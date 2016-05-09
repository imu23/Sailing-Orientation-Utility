## Processing Temperature Data

from Adafruit_I2C import Adafruit_I2C

class temp_processor(object):
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


	def calibrate(self, device):
	
		self.ac1 = device.readS16(self.BMP180_CAL_AC1, False)
		self.ac2 = device.readS16(self.BMP180_CAL_AC2, False)
		self.ac3 = device.readS16(self.BMP180_CAL_AC3, False)
		self.ac4 = device.readS16(self.BMP180_CAL_AC4, False)
		self.ac5 = device.readS16(self.BMP180_CAL_AC5, False)
		self.ac6 = device.readS16(self.BMP180_CAL_AC6, False)
		self.b1 = device.readS16(self.BMP180_CAL_B1, False)
		self.b2 = device.readS16(self.BMP180_CAL_B2, False)
		self.mb = device.readS16(self.BMP180_CAL_MB, False)
		self.mc = device.readS16(self.BMP180_CAL_MC, False)
		self.md = device.readS16(self.BMP180_CAL_MD, False)
    
    
	def procTemp(self, raw_temp):
      
		# bit manipulation
		
		X1 = (int(raw_temp - self.ac6) * self.ac5) >> 15
		X2 = (self.mc << 11) / (X1 + self.md)
		B5 = X1 + X2
		temp = ((B5 + 8) >> 4) / 10.0
    
		return temp
    
if __name__ == '__main__':
    print procTemp(0)
