## Calibrating BMP180
#   EHH

import math

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


def calibrate():
	calib = [ self._device.readS16BE(BMP180_CAL_AC1), 
	self._device.readS16BE(BMP180_CAL_AC2),
	self._device.readS16BE(BMP180_CAL_AC3),
	self._device.readU16BE(BMP180_CAL_AC4),
	self._device.readU16BE(BMP180_CAL_AC5),
	self._device.readU16BE(BMP180_CAL_AC6),
	self._device.readS16BE(BMP180_CAL_B1),
	self._device.readS16BE(BMP180_CAL_B2),
	self._device.readS16BE(BMP180_CAL_MB),
	self._device.readS16BE(BMP180_CAL_MC),
	self._device.readS16BE(BMP180_CAL_MD) ]
	

    
