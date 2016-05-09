#  Process data input
#
#  Most of the data uses the "better_process" function, which just uses
#  an exponential smoothing equation. An actually better way to smooth 
#  the data might be to compare to other data types. For example, if the
#  speed is changing but the GPS coordinates are not, one of those is probably wrong.
#
#  Note that time and date are not smoothed. It is desired to have the most recent 
#  time appear to the user. 

import math
import process_bmp
import process_compass
import process_press_extra
import process_gyro
import process_ag
import dataFormat

import sys
sys.path.insert(0, '/home/pi/SensorMain/database')
import dbLink
import dbConnect


class Processor(object):
    
    def __init__(self, db, bmp):
        print "Processor"
        self.db = db
        self.bmp = bmp
        self.prev_data = "None"
        self.prev_index = 1
        
    def setBMP(self, bmp):
        self.bmp = bmp

        
    # Order of items in raw database:
    # (date, time, lat, lon, alt, speed, temp, pressure, aX, aY, aZ, cX, cY, cZ, gyX, gyY, gyZ)
    def process(self, index):
        print "Processing"
        cursor = self.db.cursor()
        
        cursor.execute("SELECT * FROM rawEX")
        count = cursor.rowcount

        
        row = []
        date = []
        time = []
        lat = []
        lon = []
        altitude = []
        speed = []
        temperature = []
        pressure = []
        heading = []
        gyroscope = []
        acceler = []
        acc_angle = []
        
        gyr_rate = [0,0,0]
        cf_angle = [0,0,0]
        
        for x in range(self.prev_index, count):
            instr = "SELECT * FROM rawEX WHERE ID = %s" % (x)
            cursor.execute(instr)
            line = cursor.fetchone()
            
            row.append( line[0] )
            #if line[1] != None:
            #    date.append( dataFormat.convertDate("mm/dd/yyyy", 0, str(line[1])) )
            #else:
            #    date.append( line[1] )
            date.append( line[1] )
            #if line[2] != None:
            #   time.append( dataFormat.convertTime("am/pm", "EST", line[2]) )
            time.append( line[2] )
            lat.append( line[3] )
            lon.append( line[4] )
            #altitude.append( line[5] )
           
            speed.append( line[6] )
            
            temperature.append( self.bmp.procTemp(int(line[7])) )
            
            pr = self.bmp.procPress(int(line[8]), int(line[7]))
          
            altitude.append( process_press_extra.getAltitude(pr) )
            pressure.append( pr )
        
            accel = [ line[9], line[10], line[11] ]
            mag = [ line[12], line[13], line[14] ]
            gyro = [ line[15], line[16], line[17] ]
            
            heading.append(process_compass.getMag(accel, mag))
            gyroscope.append(process_gyro.accumGyro(gyro,gyr_rate))
            gyr_rate = [ gyroscope[0][0], gyroscope[0][1], gyroscope[0][2] ]
            cf_angle = process_ag.getAG( accel, cf_angle, gyr_rate )
            acceler.append( cf_angle )
            
            
        
        #print row
        #print date
        #print time
        #print lat
        #print lon
        #print altitude
        #print speed
        #print temperature
        #print pressure
        #print heading
        #print gyroscope
        #print acceler
        
        ret_date = self.err_process( date )
        ret_time = self.err_process( time )
        ret_lat = self.better_process( lat )
        ret_lon = self.better_process( lon )
        ret_alt = self.better_process( altitude )
        ret_sp = self.better_process( speed )
        ret_temp = self.better_process( temperature )
        ret_press = self.better_process( pressure )
        ret_head = self.better_process( heading )
        ret_gy = self.err_process( gyroscope )
        ret_ac = self.err_process( acceler )
        
        self.prev_index = count
        
        print "End processing"
        
        
        ret = [ ret_date, ret_time, ret_lat, ret_lon, ret_alt, ret_sp, ret_temp, ret_press, ret_head, ret_gy, ret_ac, count ]
        self.prev_data = ret
        return ret
        
    def err_process(self,   data):
        length = len(data)
        if length >= 1:
            return data[length-1]
        else:
            return "---"
            
    def better_process(self, data):
        length = len(data)
        a = 0.8
        datum = float(data[0])
        if length >= 3:
            for i in range(1, length):
                datum = a*data[i-1] + (1 - a)*datum
        return float(datum)
            
        
if __name__ == '__main__':
    
    db = dbConnect.connect()
    dbLink.createRawTable(db)
    p = Processor(db)
    p.process(0)
