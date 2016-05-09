## Main script with threading

# python script imports
import datetime
import os
import RPi.GPIO as GPIO
import signal
import sys
import threading
import time

sys.path.insert(0, '/home/pi/SensorMain/sensors')
# sensor imports
import accel
import dataFormat
import gpsPoll
import gyro
import mag
import press
import process
import process_bmp
import process_press_extra
import temp

# display imports
import edisplay


# database imports
sys.path.insert(0, '/home/pi/SensorMain/database')
import dbLink
import dbConnect

from multiprocessing import *
from threading import Thread


class threadingMain():
    def __init__(self):
        #GPIO Setup
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(12,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(22,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
        
        GPIO.add_event_detect(12, GPIO.RISING, callback=self.buttonEvent, bouncetime=1000)
        GPIO.add_event_detect(22, GPIO.RISING, callback=self.saveEvent, bouncetime=1000)
        
        #Sensor Instantiation
        self.accSensor   = accel.Accelerometer()
        self.magSensor   = mag.Magnetometer()
        self.gyroSensor  = gyro.Gyroscope()
        self.pressSensor = press.Pressure()
        self.tempSensor  = temp.Temperature()

        #Calibrate
        self.cal = process_bmp.bmp_processor()
        self.cal.calibrate(self.pressSensor.press)

        #Create the databases
        self.db = dbConnect.connect()
        dbLink.createRawTable(self.db)
        dbLink.createProcessedTable(self.db)
        dbLink.createSaveTable(self.db)
        dbLink.createDateTime(self.db)
    
        #Processor
        self.processor = process.Processor(self.db, self.cal)
        self.last_index = 0
        
        #Set the GPS poller
        self.gpsP = gpsPoll.GpsPoller()

        self.common_delay_time = 0.5
        
        #Initialize the display
        self.edisplay = edisplay.EDisplay()
        
        #Initialize sensor vars
        self.acc = 0
        self.gyro = 0
        self.temp = 0
        self.press = 0
        self.mag = 0
        
        #Initialize gps vars
        self.date = 0
        self.time = 0
        self.lat = 0
        self.lon = 0
        self.speed = 0
        self.alt = 0
        
        self.key_in = 0
        
        self.disp_data = [0,0,0,0,0,0,0,0,0,0,0]
        self.saving_text = "no"
        
        
        self.start_data = True
        self.saving_flag = "no"
        #Initialize saving vars
        self.saving = False
        self.saveStartTime = 0
        self.saveStartDate = 0
        self.saveEndTime = 0
        self.saveEndDate = 0
        
    
    def get_temp(self, delay):
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            #print "#1"
            temp_time_st = int((datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).total_seconds() *1000)
            self.temp = self.tempSensor.read()
            temp_time_end = int((datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).total_seconds() *1000)
            #print "t el: ", (temp_time_end - temp_time_st)
            time.sleep(delay)
            
    def get_press(self, delay):
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            #print "#2"
            press_time_st = int((datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).total_seconds() *1000)
            self.press = self.pressSensor.read()
            press_time_end = int((datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).total_seconds() *1000)
            #print "p el: ", (press_time_end - press_time_st)
            time.sleep(delay)
            
    def get_temp_press(self, delay):
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            #print "#15"
            self.temp = self.tempSensor.read()
            self.press = self.pressSensor.read()
            time.sleep(delay)
            
    def get_mag(self, delay):
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            #print "#3"
            mag_time_st = int((datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).total_seconds() *1000)
            self.mag = self.magSensor.read()
            mag_time_end = int((datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).total_seconds() *1000)
            #print "m el: ", (mag_time_end - mag_time_st)
            time.sleep(delay)
     
    def get_acc(self, delay):
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            #print "#4"
            acc_time_st = int((datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).total_seconds() *1000)
            self.acc = self.accSensor.read()
            acc_time_end = int((datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).total_seconds() *1000)
            #print "a el: ", (acc_time_end - acc_time_st)
            time.sleep(delay)
            
    def get_gyro(self, delay):
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            #print "#5"
            gyro_time_st = int((datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).total_seconds() *1000)
            self.gyro = self.gyroSensor.read()
            gyro_time_end = int((datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).total_seconds() *1000)
            #print "g el: ", (gyro_time_end - gyro_time_st)
            time.sleep(delay) 
    ######        
    # GPS FUNCTIONS: 
    # Choose either get_gps_next_all() to perform a get_next() from the gpsd and all the values,
    # or do some combination of the below functions. If the second method is chosen, some 
    # editing may need to be done with the functions to have the threading aspect work properly.
    ######
    def get_gps_next(self, delay):
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            print "6"
            gps_time_st = int((datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).total_seconds() *1000)
            self.gpsP.getNext()
            gps_time_end = int((datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).total_seconds() *1000)
            #print "gps el: ", (gps_time_end - gps_time_st)
            time.sleep(delay) 
            
    def get_date(self, delay):
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            #print "#7"
            self.date = self.gpsP.getDate()
            time.sleep(delay)
    
    def get_time(self, delay):
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            #print "#8"
            self.time = self.gpsP.getTime()
            time.sleep(delay)
    
    def get_lat(self, delay):
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            #print "#9"
            self.lat = self.gpsP.getLat()
            time.sleep(delay)
    
    def get_lon(self, delay):
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            #print "#10"
            self.lon = self.gpsP.getLong()
            time.sleep(delay)
            
    def get_Alt(self, delay):
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            #print "#11"
            self.alt = self.gpsP.getAlt()
            time.sleep(delay)
            
    def get_speed(self, delay):
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            #print "#12"
            self.speed = self.gpsP.getSpeed()
            time.sleep(delay)
    
    def get_all_gps(self, delay):
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            #print "#13"
            self.date = self.gpsP.getDate()
            self.time = self.gpsP.getTime()
            self.lat = self.gpsP.getLat()
            self.lon = self.gpsP.getLong()
            self.alt = self.gpsP.getAlt()
            self.speed = self.gpsP.getSpeed()
            time.sleep(delay)
            
    def get_next_all_gps(self, delay):
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            #print "#14"
            self.gpsP.getNext()
            self.date = self.gpsP.getDate()
            self.time = self.gpsP.getTime()
            self.lat = self.gpsP.getLat()
            self.lon = self.gpsP.getLong()
            #self.alt = self.gpsP.getAlt()
            self.speed = self.gpsP.getSpeed()
            time.sleep(delay)
      
     # DISPLAY
    def display(self, delay):
         t = threading.currentThread()
         while getattr(t, "do_run", True):
             #os.system('clear')
             #print "#d"
             # Process return data
        # 0: date
        # 1: time
        # 2: lat
        # 3: lon
        # 4: alt
        # 5: speed
        # 6: temp
        # 7: press
        # 8: heading
        # 9: gyro
        #10: accel
             try:
                self.disp_data[0] = dataFormat.convertDate("mm/dd/yy", "EDT", self.disp_data[0])
             except:
                 print "Failed to convert Date"
                 
             try:
                self.disp_data[1] = dataFormat.convertTime("am/pm", "EDT", self.disp_data[1])
             except:
                 print "Failed to convert Time"
             
             print "Date:  ", self.disp_data[0]
             print "Time:  ", self.disp_data[1]
             print "Lat:   ", self.disp_data[2]
             print "Lon:   ", self.disp_data[3]
             
             try:
                self.disp_data[4] = dataFormat.convertAltitude("meters", self.disp_data[4])
             except:
                 print "Failed to convert Alititude"
                 
             print "Alt:   ", self.disp_data[4]
             
             try:
                self.disp_data[5] = dataFormat.convertSpeed("mph", self.disp_data[5])
             except:
                 print "Failed to convert Speed"
                 
             print "Speed: ", self.disp_data[5]
             
             try:
                self.disp_data[6] = dataFormat.convertTemp("F", self.disp_data[6])
             except:
                 print "Failed to convert Temp"
                 
             print "Temp:  ", self.disp_data[6]
             
             try:
                self.disp_data[7] = dataFormat.convertPressure("kPa", self.disp_data[7])
             except:
                 print "Failed to convert Pressure"
             print "Press: ", self.disp_data[7]
             
            #try:
            #    self.disp_data[8] = dataFormat.convertHeading("16", self.disp_data[8])
            # except:
            #    print "Failed to convert Heading"
             
             print "Head:  ", self.disp_data[8]
             #print "Gyro:  ", self.disp_data[9]
             #print "Accel: ", self.disp_data[10]

             self.edisplay.display_data(self.disp_data, self.saving_text)
             
             time.sleep(delay)
             
    # Call processor and save
    def process(self, counter):
        self.disp_data = self.processor.process(counter)
        self.last_index = self.disp_data[11]
        if self.saving:
            dbLink.insertSaving(self.db, self.disp_data)
        return self.disp_data
        
    # Respond to button 1 event (change screens)
    def buttonEvent(self, channel):
        print "Change screens"
        if(self.edisplay.pause):
            self.edisplay.pause = False
        else:
            self.edisplay.pause = True
    # Respond to button 2 event (start data, start/stop saving)
    #   Once the data has started to be collected, the button functionality switches
    def saveEvent(self, channel):
        if self.start_data == False:
            print "Starting data"
            self.start_data = True
        else:
            print "Saving toggled"
            if self.saving:
                print "On -> Off"
                self.saving_text = "no"
                # get end date and time
                self.saveEndDate = self.date
                self.saveEndTime = self.time
                # store start/end date/time in saving table
                dbLink.insertLogDateTime(self.db, self.saveStartDate, self.saveStartTime, self.saveEndDate, self.saveEndTime)
                self.saving = False
            else:
                print "Off -> On"
                self.saving_text = "yes"
                # get start date and time
                self.saveStartDate = self.date
                self.saveStartTime = self.time
                self.saving = True
            
            

    
            
            
if __name__ == '__main__':
    try:
        main = threadingMain()
        
        # Process return data
        # 0: date
        # 1: time
        # 2: lat
        # 3: lon
        # 4: alt
        # 5: speed
        # 6: temp
        # 7: press
        # 8: heading
        # 9: gyro
        #10: accel

        # Show the display startup screen
        main.edisplay.display_startup()
        
        # Wait for start button event
        while main.start_data == False:
            time.sleep(1)
       
        # Initialize threads
        #  Second argument is the time delay between sensor reads. 
        #  GPS takes the longest (~450ms? varies.) to actually read
        thr1 = Thread(target=main.get_temp, args=[0.5]) # temp
        thr2 = Thread(target=main.get_press, args=[0.5]) # press
        thr3 = Thread(target=main.get_mag, args=[0.5])  # mag
        thr4 = Thread(target=main.get_acc, args=[0.5])  # acc
        thr5 = Thread(target=main.get_gyro, args=[0.5]) # gyro
        # Select desired method of retrieving GPS data
        thr6 = Thread(target=main.get_next_all_gps, args=[0.5]) #gps
        # Display the RAW data in a terminal
        thr7 = Thread(target=main.display, args=[0.5])
           
        threads = [thr1, thr2, thr3, thr4, thr5, thr6, thr7]
    
    
        # Start the threads to begin collecting data and updating the screen, etc.
        print "Starting sensors..."
        for i in range(0,7):
            threads[i].start()
        
        # Initialize counter to process at a set interval
        count = 0
        
        while True:
           # time_st = int((datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).total_seconds() *1000)
           # print "temp: ", main.temp
           # print "press: ", main.press
           # print "mag: ", main.mag
           # print "acc: ", main.acc
           # print "gyro: ", main.gyro
           # print "date: ", main.date
           # time_end = int((datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).total_seconds() *1000)
            # Add to the database
            dbLink.insertRawEX(main.db, main.date, main.time, main.lat, main.lon, main.alt, main.speed, main.temp, main.press, main.acc[0], main.acc[1], main.acc[2], main.mag[0], main.mag[1], main.mag[2], main.gyro[0], main.gyro[1], main.gyro[2]) 
            # After 5 reads, process new data
            if count > 5:
                main.process(count)
                #print main.disp_data
                count = 0
            count = count + 1
            # sleep for a bit before adding to database again -- this is where the interrupt (below) will be able to work
            time.sleep(0.8)
    # Stop threads and program itself on break (ctrl+c)
    except (KeyboardInterrupt, SystemExit):
        GPIO.cleanup()
        for i in range(0,7):
            threads[i].do_run = False
        
        # There's no point in joining them now
        
        #for i in range(0,6):
        #   print "joining"
        #   threads[i].join()
        try:
            sys.exit(0)
        except (SystemExit):
            os.kill(os.getpid(), signal.SIGKILL)
        
