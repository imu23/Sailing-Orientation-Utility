## Converting Accelerometer and Gyroscope Data

import math
    
def getAG(accel, accel_ang, gyr_rate):
    
    # smoothing constant
    aa = .98
    # Delay Time constant
    dt = .05
    
    # Calculate CF Angles X and Y
    cf_angle_x = ( aa * accel_ang[0] + gyr_rate[0] * dt ) + ( 1 - aa ) * accel[0]
    cf_angle_y = ( aa * accel_ang[1] + gyr_rate[1] * dt ) + ( 1 - aa ) * accel[1]
    
    acc = [ cf_angle_x, cf_angle_y ]
    
    return acc
    
if __name__ == '__main__':
    import accel
    
    from time import sleep
    from os import system
    
    ac = accel.Accelerometer()
    
    sleeptime = 0.5
    
    while True:
        system('clear')
        print getAG(ac.read())
        sleep(sleeptime)
