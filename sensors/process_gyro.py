## Accumulating Gyroscope Data

import math
    
def accumGyro(g_raw, g_angle):

	# gain
    gain = 0.07
	
	# time lapse interval
    dt = 0.05
    
    # Gyroscope to degrees
    g_rate_x = float(g_raw[0]*gain)
    g_rate_y = float(g_raw[1]*gain)
    g_rate_z = float(g_raw[2]*gain)
    
    g_angle[0] = g_angle[0] + (g_rate_x * dt)
    g_angle[1] = g_angle[1] + (g_rate_y * dt)
    g_angle[2] = g_angle[2] + (g_rate_z * dt)
    
    gyro_ret = [ g_rate_x, g_rate_y, g_rate_z, g_angle[0], g_angle[1], g_angle[2] ]
    return gyro_ret
    
if __name__ == '__main__':
    import gyro
    
    from time import sleep
    from os import system
    
    gy = gyro.Gyroscope()
    
    sleeptime = 0.5
    
    gyr = [0,0,0]
    while True:
        system('clear')
        print accumGyro(gy.read(), gyr)
        sleep(sleeptime)
