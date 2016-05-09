## Converting Accelerometer Data
#   EHH

import math
    
def getAccel(accel):
    
    # Accelerometer to degrees
    accXangle = math.degrees(float( math.atan2(accel[1], accel[2]) + math.pi ))
    accYangle = math.degrees(float( math.atan2(accel[2], accel[0]) + math.pi ))
    
    # Accel to +/-180
    if ( accXangle > 180 ):
        accXangle = accXangle - 360.0
    
    if ( accYangle > 180 ):
        accYangle = accYangle - 360.0
    
    acc = [ accXangle, accYangle ]
    return acc
    
if __name__ == '__main__':
    import accel
    
    from time import sleep
    from os import system
    
    ac = accel.Accelerometer()
    
    sleeptime = 0.5
    
    while True:
        system('clear')
        print getAccel(ac.read())
        sleep(sleeptime)
