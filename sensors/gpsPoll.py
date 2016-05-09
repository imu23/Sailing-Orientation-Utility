#! /usr/bin/python
# Adapted from Dan Mandle http://dan.mandle.me September 2012
# License: GPL 2.0

import os
from gps import *
from time import *
from decimal import *
import time
from dataFormat import *
gpsd = None #setting the global variable

#os.system('clear') #clear the terminal (optional)
 
class GpsPoller(object):
  def __init__(self):
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    
  def getNext(self):
	gpsd.next()

  def getLat(self):
    global gpsd
    return Decimal(gpsd.fix.latitude)  
     
  def getLong(self):
    return Decimal(gpsd.fix.longitude)

  def getSpeed(self):
    return Decimal(gpsd.fix.speed)

  def getTime(self):
    return gpsd.utc[11:-5]

  def getDate(self):
    return gpsd.utc[:10]
    
  def getAlt(self):
	return Decimal(gpsd.fix.altitude)

if __name__ == '__main__':
  gpsp = GpsPoller() # create the thread
  try:
    gpsp.start() # start it up
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    #text_file.close()
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
  print "Done.\nExiting."



