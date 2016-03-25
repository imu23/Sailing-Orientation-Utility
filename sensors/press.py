## Pressure Raw Data Collector
#    EHH

from Adafruit_I2C import Adafruit_I2C
import time

class Pressure(Adafruit_I2C):
    
    # Assign registers
    BMP180_I2CADDR           = 0x77
    
    # BMP180 Registers
    BMP180_CONTROL           = 0xF4
    BMP180_OUTMSB            = 0xF6
    

    # Commands
    # Read pressure data command: 0x34

    def __init__(self, busnum=-1, debug=False, hires=False):
        # Create new I2C instance
        self.press = Adafruit_I2C(self.BMP180_I2CADDR, busnum, debug)
        
        # Enable the pressure sensor
        # self.press.write8(self.BMP085_CONTROL, 0x34)
        # Have to wait? Do this in a proc
        
    # Interpret signed 16-bit temperature component from list
    def press16(self, list, idx):
        n = (list[idx] << 8) | list[idx+1]   # High, low bytes
        return n if n < 32768 else n - 65536 # 2's complement signed
        
    def read(self, mode=1):
        # Read the pressure
        self.press.write8(self.BMP180_CONTROL, 0x34)
        # have to wait depending on mode before reading
        if mode == 0:
            time.sleep(0.005)
        elif mode == 1:
            time.sleep(0.008)
        elif mode == 2:
            time.sleep(0.014)
        else:
            time.sleep(0.026)
            
        msb = self.press.readU8(self.BMP180_OUTMSB)
        lsb = self.press.readU8(self.BMP180_OUTMSB+1)
        xlsb = self.press.readU8(self.BMP180_OUTMSB+2)
        
        res = ((msb << 16) + (lsb << 8) + xlsb) >> (8 - mode)
        
        return res
        
if __name__ == '__main__':
    
    from time import sleep
    import os
    import temp
    
    import process_bmp as pt
    
    import process_press_extra as pe
    
    press = Pressure()
    temp = temp.Temperature()
    
    proc = pt.bmp_processor()
    proc.calibrate(press.press)
    timer = 0
    sleeptime = 0.5
 
    
    while True:
        os.system('clear')
        m = press.read()
        t = temp.read()
        print "Raw press: ", m
        print "Raw temp : ", t
        pr = proc.procPress(m,t)
        te = proc.procTemp(t)
        print "Press: ", pr
        print "Temp : ", te
        alt = pe.getAltitude(pr)
        print "Alt: ", alt
        print "Sealevel press: ", pe.getSealevelPress(pr, alt)
        sleep(sleeptime)

