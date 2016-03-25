## Converting Magnetometer Data
#	EHH

import math

# Import own files
import accel as ac
import mag as mg
    
def getMag():
	
	accelInst = ac.Accelerometer()
	magInst = mg.Magnetometer()
	
	accel = accelInst.read()
	mag = magInst.read()
    
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
	print getMag()
