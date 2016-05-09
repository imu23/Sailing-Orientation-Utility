# Format different data types according to the specified format.
#

import os
from gps import *
from time import *
from decimal import *
from dataFormat import *
import time
import threading
import string
 
CON_VAL = Decimal(3600)/Decimal(1852)

#Converts meters/second to nautical miles/hour
def toKnot(x):
    knots = CON_VAL * Decimal(x)
    return knots

#+++++++++++++++++ Speed ++++++++++++++++++++++++
# Convert speed into "m/s", "mph", "knots", or "kmhr".
def convertSpeed(form, x):
    if form == "m/s":
        return '{0:0.2f} m/s'.format(x)
    if form == "mph":
        return '{0:0.2f} mph'.format(x*3600/1609.34)
    if form == "knots":
        return '{0:0.2f} knots'.format(toKnot(x))
    if form == "kmhr":
        return '{0:0.2f} kmhr'.format(x*18/5)

#+++++++++++++++++ Date ++++++++++++++++++++++++
# Convert the decimal compass heading data into compass directions.
# Format can be "8", "16", or "deg".
# 8 results in directions: N, NE, E, SE, S, SW, W, NW
# 16 results in directions: N, NNE, NE, ENE, E, ESE, SE, SSE, S, SSW, SW,
#   WSW, W, WNW, NW, NNW
def convertHeading(form, x):
    if form == "8":
        if x >= 337.5 and x <= 22.5:
            return "N"
        if x > 22.5 and x < 67.5:
            return "NE"
        if x >= 67.5 and x <= 112.5:
            return "E"
        if x > 112.5 and x < 157.5:
            return "SE"
        if x >= 157.5 and x <= 202.5:
            return "S"
        if x > 202.5 and x < 247.5:
            return "SW"
        if x >= 247.5 and x <= 292.5:
            return "W"
        if x > 292.5 and x < 337.5:
            return "NW"
    if form == "16":
        if x >= 348.75 and x <= 11.25:
            return "N"
        if x > 11.25 and x < 33.75:
            return 'NNE'
        if x >= 33.75 and x <= 56.25:
            return  'NE'
        if x > 56.25 and x < 78.75:
            return 'ENE'
        if x >= 78.75 and x <= 101.25:
            return 'E'
        if x > 101.25 and x < 123.75:
            return 'ESE'
        if x >= 123.75 and x <= 146.25:
            return 'SE'
        if x > 146.25 and x < 18.75:
            return 'SSE'
        if x >= 168.7 and x <= 191.25:
            return 'S'
        if x > 191.25  and x < 213.75:
            return 'SSW'
        if x >= 213.75 and x <= 236.25:
            return 'SW'
        if x > 236.25 and x < 258.75:
            return 'WSW'
        if x >= 258.75 and x <= 281.25:
            return 'W'
        if x > 281.25 and x <  303.75:
            return 'WNW'
        if x >= 303.75 and x <= 326.26:
            return 'NW'
        if x > 326.25 and x < 348.75:
            return 'NNW'
    if form == "deg":
        return x 

#+++++++++++++++++ Time ++++++++++++++++++++++++
# Format the time 
def getTime(x):
    time = x[11:-5]
    return time

# Get the timezone difference to alter the time from the GPS
# Timezones include: "EDT", "EST", "CST", "MST", and "PST".
# More can easily be added. 
def tzDiff( tz ):    
    if tz == "EDT":
        return -4
    elif tz == "EST" or tz == "CDT":
        return -5
    elif tz == "CST" or tz == "MDT":
        return -6
    elif tz == "MST" or tz == "PDT":
        return -7
    elif tz == "PST":
        return -8

# Apply the timezone change to the current GPS time
def tzCChange(x, tz):
    #print "tz x: ", x
    strTime = str(x[:2])
    #print "tz strTime: ", strTime
    delta = tzDiff( tz )
    #print "tzDiff: ", delta
    try:
        time = int(strTime)
        time += delta
        if time < 0:
            time += 24
        #print "try time: ", time
    except ValueError:
        #print "valerror"
        time = 0
    #print "returning: ", str(time) + x[2:]
    return str(time) + x[2:]


def convertTime(form, tz, x):
	x = str(x)
	x = string.strip(x)
	seg = x.split(":")
	diff = tzDiff(tz)
	x1 = Decimal(seg[0])
	x2 = Decimal(seg[1])
	x3 = Decimal(seg[2])
	x1 = x1 + diff
	ampm = "am"
	if form == "am/pm":
		if x1 > 12:
			x1 = 24 - x1
		if x1 < 0:
			x1 = 12 + x1
			ampm = "pm"
		elif x1 > 12 :
			x1 = 12 - x1
			ampm = "pm"
		else:
			ampm = "am"
		newTime = '{:02f}:{:02f}:{:02f} {}'.format(x1, x2, x3, ampm)
		return newTime
	return x


# Convert the time based on specified format and timezone
# Formats are "am/pm" or else will be in military time
def convertTTime(form, tz, x):
    x = str(x)
    print "time: ", x
    x1 = string.strip(x)
    print "x1: ", x1
    time = x[11:-5]
    print "x: ", x
    time = x
    if tz == "UTC":
        return time
    time = tzChange( time, tz )
    print "time: ", time
    if form == "am/pm":
        strTime = "0" + str(time[:2])
        if strTime[2:3] == ":" :
            #print "colon"
            strTime = strTime[0:2]
            #print "new: ", strTime
            time = time[2:]
            #print "tt: ", time
        else:
            time = time[3:]
            #print "tt: ", time
        #print "strTime ", strTime
        period = "AM"
        try:
            t = int(strTime)
            #print "t: ", t
            if t > 12:
                t -= 12
                period ="PM"
        except ValueError:
            #print "valueerror2"
            t = 0
        #print "time[2:]", time[2:]
        #print "returning: ", str(t) + ":" + time + " " + period
        return str(t) + ":" + time + " " + period
    else:
        return time

#+++++++++++++++++ Date ++++++++++++++++++++++++
# Convert the date based on the format and timezone
# Formats include: "mm/dd/yy", "dd/mm/yyyy", and "yyyymmdd"
def convertDate(form, tz, x):
    if x == 0:
        return "----"
    x = str(x)
    date = x[:10]
    d = date[8:]
    m = date[5:7]
    y = date[:4]
    if form == "mm/dd/yy":
        return m + "/" + d + "/" + y
    if form == "dd/mm/yyyy":
        return d + "/" + m + "/" + y
    if form == "yyyymmdd":
        return y + m + d

# Checks if the GPS datetime is still "today" based on timezone
def isToday( x, tz ):
    if tz == "UTC":
        return 0
    time = tzChange( x[11:-5], tz )
    try: 
        hour = time[:2]
        intHour = int(hour)
        if( (intHour + (-1*tzDiff(tz))) > 24 ):
            return 1
    except ValueError:
        hour = 0
    return 0

#+++++++++++++++++ Temp ++++++++++++++++++++++++
# Convert the temperature
# Formats include: "C", "K", and "F"
def convertTemp(form, x):
    if form == "C":
        return '{0:0.2f} C'.format( x )
    if form == "K":
        return '{0:0.2f} K'.format( x + 273.15)
    if form == "F":
        return '{0:0.2f} F'.format((x*1.8)+32)

#+++++++++++++++++ Pressure ++++++++++++++++++++++++
# Convert the pressure
# Formats include: "inHg", "mmHg", "kPa", and "atm"
def convertPressure(form, x):
    if form == "inHg":
        return '{0:0.2f} inHg'.format( x/3386.375258 )
    if form == "mmHg":
        return '{0:0.2f} mmHg'.format( x/133.322365 )
    if form == "kPa":
        return '{0:0.2f} kPa'.format(x/1000.0)
    if form == "atm":
        return '{0:0.2f} atm'.format(x/101325.0)

#+++++++++++++++++ Altitude ++++++++++++++++++++++++
def convertAltitude(form, x):
    if form == "meters":
        return '{0:0.2f} m'.format(x)
    if form == "feet":
        return '{0:0.2f} ft'.format(x*3.2808)

#+++++++++++++++++ Long/Lat ++++++++++++++++++++++++
def deg2dms(z):
    z = abs(z)
    d = int(z) #whole number degree value
    temp = Decimal(z)-Decimal(d) #remainder of degree value
    m = int(temp*60) #whole number minute value
    s = int(((temp*60) - m)*60) #whole seconds value
    dms = str(d) + '*'+ str(m) + '\'' + str(s) + '\"'
    return dms

def longDir(x):
    if x < 0:
        return ' W '
    return ' E '

def latDir(x):
    if x < 0:
        return ' S '
    return ' N '

def convertLong( form, x ):
    if form == "DMS":
        dms = deg2dms( x ) + longDir( x )
        return dms
    if form == "dec":
        return x

def convertLat( form, x ):
    if form == "DMS":
        dms = deg2dms( x ) + latDir( x )
        return dms
    if form == "dec":
        return x
