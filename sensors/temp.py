## Temperature Raw Data Collector
#    EHH

from Adafruit_I2C import Adafruit_I2C
import time

class Temperature(Adafruit_I2C):
    
    # Assign registers
    BMP180_I2CADDR           = 0x77
    
    # BMP180 Registers
    BMP180_CONTROL           = 0xF4
    BMP180_OUTMSB            = 0xF6
    

    # Commands
    # Read temp data command: 0x2E

    def __init__(self, busnum=-1, debug=False, hires=False):
        # Create new I2C instance
        self.temp = Adafruit_I2C(self.BMP180_I2CADDR, busnum, debug)
        
        # Enable the temperature sensor
        # self.temp.write8(self.BMP180_CONTROL, 0x2E)
        # Need to wait before reading
        
    # Interpret signed 16-bit temperature component from list
    # def temp16(self, list, idx):
    #    n = (list[idx] << 8) | list[idx+1]   # High, low bytes
    #    return n if n < 32768 else n - 65536 # 2's complement signed
        
    #def process_temp(self, raw_temp):
	#	UT = raw_temp
	#	X1 = ((UT - 23153) * 32757) >> 15
	#	X2 = (-8711 << 11) / (X1 + 2868)
	#	B5 = X1 + X2
	#	temp = ((B5 + 8) >> 4) / 10.0
	#	return temp
        
    def read(self):
        # Read the temperature
        # Enable the temperature sensor
        
        self.temp.write8(self.BMP180_CONTROL, 0x2E)
        # Have to sleep 5 ms before reading
        time.sleep(0.005)
        res = self.temp.readU16(self.BMP180_OUTMSB, False)
        
        return res
        
if __name__ == '__main__':
	
	from time import sleep
	import os
	
	import process_temp as pt
	
	temp = Temperature()
	proc = pt.temp_processor()
	proc.calibrate(temp.temp)
	timer = 0
	sleeptime = 0.5
	
	while True:
		os.system('clear')
		m = temp.read()
		print m
		t = proc.procTemp(m)
		print t
		sleep(sleeptime)

