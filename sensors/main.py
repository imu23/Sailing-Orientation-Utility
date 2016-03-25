'''
Sailing Orientation
Senior Project 2016

Alexander Clarke
Eliza Hunt-Hawkins
Ian Powell
Kim Tran

Main script that polls data from all the sensors and inserts it into the DB.
'''

#imports


#import gpsPoll
import time
from time import *
import accel
import mag
import gyro
#import temp
import press

import sys
sys.path.insert(0, '../database')
import dbLink
import dbConnect

#Sensor Instantiation
accSensor   = accel.Accelerometer()
magSensor   = mag.Magnetometer()
gyroSensor  = gyro.Gyroscope()
pressSensor = press.Pressure()
#tempSensor  = temp.Temperature()


#Create the databases
db = dbConnect.connect()
dbLink.createRawTable(db)
dbLink.createProcessedTable(db)

#gpsP = gpsPoll.GpsPoller()

while True:

    #Accel[x,y,z]
    acc = accSensor.read()
    
    #Gyro[x,y,z]
    gyro = gyroSensor.read()

    #Mag[x,y,z]
    mag = magSensor.read()

    #def insertRawEX(db, date, time, lat, longitude, alt, speed, temp, aX, aY, aZ, cX, cY, cZ, gyX, gyY, gyZ):
    dbLink.insertRawEX(db, "2016-12-12", "22:22:22", "44", "44", "44", "44", "44", acc[0], acc[1], acc[2], mag[0], mag[1], mag[2], gyro[0], gyro[1], gyro[2]) 
    dbLink.getRawEX(db);
