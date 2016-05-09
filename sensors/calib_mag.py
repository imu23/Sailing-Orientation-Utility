## Calibrate the magenetometer readings
#  Fair warning: this output is awful. Don't use it if you care
#  about things like that, or clean it up first.

import mag

maxX = 0
minX = 0
maxY = 0
minY = 0
maxZ = 0
minZ = 0

mg = mag.Magnetometer()


while True:
	m = mg.read()
	if m[0] < minX:
		minX = m[0]
	if m[0] > maxX:
		maxX = m[0]
		
	if m[1] < minY:
		minY = m[1]
	if m[1] > maxY:
		maxY = m[1]
	
	if m[2] < minZ:
		minZ = m[2]
	if m[2] > maxZ:
		maxZ = m[2]
		
	print "minX: ", minX
	print "maxX: ", maxX
	print "minY: ", minY
	print "maxY: ", maxY
	print "minZ: ", minZ
	print "maxZ: ", maxZ
		
