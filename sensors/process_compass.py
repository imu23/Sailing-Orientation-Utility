## Converting Magnetometer Data
#	EHH

import math
    
def getMag(accel, mag):
    
	# NEED TO CALIBRATE TO GET THESE ACTUAL VALUES
	magMinX = -544
	magMaxX = 544
	magMinY = -544
	magMaxY = 544
	magMinZ = -544
	magMaxZ = 544

	# normalized acceleration values:
	den = float( accel[0]*accel[0] + accel[1]*accel[1] + accel[2]*accel[2] )
	axn = accel[0] / math.sqrt(den)
	ayn = accel[1] / math.sqrt(den)
	azn = accel[2] / math.sqrt(den)

	pitch = math.asin(-1*axn)
	roll = math.asin(ayn/(math.cos(pitch)))

	mxc = (mag[0]-magMinX) / (magMaxX - magMinX) * 2 -1
	myc = (mag[1]-magMinY) / (magMaxY - magMinY) * 2 -1
	mzc = (mag[2]-magMinZ) / (magMaxZ - magMinZ) * 2 -1

	magX = mxc * math.cos(pitch) + mzc * math.sin(pitch)
	magY = mxc * math.sin(roll) * math.sin(pitch) + myc * math.cos(roll) - mzc * math.sin(roll) * math.cos(pitch)

	heading = math.degrees(math.atan2(magY, magX))

	if heading < 0:
		heading = 360 + heading
	
	return heading
	
if __name__ == '__main__':
	import accel
	import mag
	
	from time import sleep
	from os import system
	
	ac = accel.Accelerometer()
	mg = mag.Magnetometer()
	
	sleeptime = 0.5
	
	while True:
		system('clear')
		print getMag(ac.read(),mg.read())
		sleep(sleeptime)
