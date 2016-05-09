#!/usr/bin/env python
import MySQLdb

# connect to the database with the root 
def connect():
    db = MySQLdb.connect('localhost', 'root', 'raspberry', 'logs')
    if db is None:
        print("Error: Unable to connect to the database")
    return db
#--------------------------------------------------------------------------------------------
# drop the rawEx table everytime it is created
def createRawTable(db):
	curs = db.cursor()

	try:
		curs.execute("""USE logs""")
		curs.execute("""DROP TABLE IF EXISTS rawEX""")
		curs.execute("""CREATE TABLE rawEX(ID int NOT NULL AUTO_INCREMENT, date DATE, time TIME, lat float, longitude float,
			alt float, speed float, temp float, pressure float, aX float, aY float, aZ float, cX float, cY float, cZ float, gyX float, gyY float, gyZ float, PRIMARY KEY(ID))""")
		db.commit()
		print "rawEX table is created"
	except: 
		print "Error Create: the database is being rolled back"
		db.rollback()

#-----------------------------------------------------------------------------------------------
def insertRawEX(db, date, time, lat, longitude, alt, speed, temp, pressure, aX, aY, aZ, cX, cY, cZ, gyX, gyY, gyZ):
	curs = db.cursor()
	
	try:
		curs.execute("""INSERT INTO rawEX (date, time, lat, longitude, alt, speed, temp, pressure, aX, aY, aZ, cX, cY, cZ, gyX, gyY, gyZ)
         	  values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (date, time, lat, longitude, alt, speed, temp, pressure, aX, aY, aZ, cX, cY, cZ, gyX, gyY, gyZ))   
		db.commit()

	except: 
		print "Error Insert: the database is being rolled back"
		db.rollback()
#-------------------------------------------------------------------------------------
# to get the rawEx table data to check data (options to use)
def getRawEX(db):
	curs = db.cursor()

	curs.execute("SELECT * FROM rawEX")
	print "\nID\tDate\tTime\tLat\tLong\tAlt\tSpeed\tTemp\tPressure\taX\taY\taZ\tcX\tcY\tcZ\tgyX\tgyY\tgyZ"
	print "=============================================================================================================================="

	for row in curs.fetchall():
		ID = str(row[0])
		date = str(row[1])
		time = str(row[2])
		lat = str(row[3])
		lon = str(row[4])
		alt = str(row[5])
		speed = str(row[6])
		temp = str(row[7])
		pressure = str(row[8])
		aX = str(row[9])
		aY = str(row[10])
		aZ = str(row[11])
		cX = str(row[12])
		cY = str(row[13])
		cZ = str(row[14])
		gyX = str(row[15])
		gyY = str(row[16])
		gyZ = str(row[17])
		
		
		print "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % \
			(ID, date, time, lat, lon, alt, speed, temp, pressure, aX, aY, aZ, cX, cY, cZ, gyX, gyY, gyZ)
		print 'Raw Pressure = {0:0.2f}'.format(sensor.read_raw_pressure())
#---------------------------------------------------------------------------------------------------
def createProcessedTable(db):
	curs = db.cursor()

	try:
		curs.execute("""USE logs""")
		curs.execute("""DROP TABLE IF EXISTS processed""")
		curs.execute("""CREATE TABLE processed(ID int NOT NULL AUTO_INCREMENT, date DATE, time TIME, lat float, longitude float,
			alt float, speed float, temp float, pressure float, aX float, aY float, aZ float, mag float, gyX float, gyY float, gyZ float, PRIMARY KEY(ID))""")
		db.commit()
		print "processed table is created"
	except: 
		print "Error: the database is being rolled back"
		db.rollback()
#----------------------------------------------------------------------------------------------
def insertProcessed(db, date, time, lat, longitude, alt, speed, temp, pressure, aX, aY, aZ, mag, gyro):
	curs = db.cursor()
   
	try:
		curs.execute("""INSERT INTO processed(date, time, lat, longitude, alt, speed, temp, pressure, aX, aY, aZ, mag, gyro)
         	  values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (date, time, lat, longitude, alt, speed, temp, pressure, aX, aY, aZ, mag, gyro))    
		db.commit()
		print "Data committed"

	except: 
		print "Error: the processed database is being rolled back"
		db.rollback()
#--------------------------------------------------------------------------------------------
def createSaveTable(db):
	curs = db.cursor()

	try:
		curs.execute("""USE logs""")
		#curs.execute("""DROP TABLE IF EXISTS saving""")
		curs.execute("""CREATE TABLE saving(ID int NOT NULL AUTO_INCREMENT, date DATE, time TIME, lat float, longitude float, alt float, speed float, temp float, pressure float, heading float, gyX float, gyY float, gyZ float, gyRateX float, gyRateY float, gyRateZ float, accelAngleX float, accelAngleY float, PRIMARY KEY(ID))""")
		db.commit()
		print "saving table is created"
	except: 
		print "Error: the saved database is being rolled back"
		db.rollback()
#----------------------------------------------------------------------------------------------
def insertSaving(db, data):
	date = data[0]
	time = data[1]
	lat = data[2]
	longitude = data[3]
	alt = data[4]
	speed = data[5]
	temp = data[6]
	pressure = data[7]
	heading = data[8]
	gyX = data[9][0]
	gyY = data[9][1]
	gyZ = data[9][2]
	gyRateX = data[9][3]
	gyRateY = data[9][4]
	gyRateZ = data[9][5]
	accelAngleX = data[10][0]
	accelAngleY = data[10][1]

	#print data
	
	
	curs = db.cursor()
   
	try:
		curs.execute("""INSERT INTO saving  (date, time, lat, longitude, alt, speed, temp, pressure, heading, gyX, gyY, gyZ, gyRateX, gyRateY, gyRateZ, accelAngleX, accelAngleY)
           values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (date, time, lat, longitude, alt, speed, temp, pressure, heading, gyX, gyY, gyZ, gyRateX, gyRateY, gyRateZ, accelAngleX, accelAngleY))   
		db.commit()
		print "Saving Data committed"

	except: 
		print "Error: the saved database is being rolled back"
		db.rollback()

#--------------------------------------------------------------------------------------------
def createDateTime(db):
	curs = db.cursor()

	try:
		curs.execute("""USE logs""")
		#curs.execute("""DROP TABLE IF EXISTS logDateTime""")
		curs.execute("""CREATE TABLE logDateTime(ID int NOT NULL AUTO_INCREMENT, startDate DATE, startTime TIME, endDate DATE, endTime TIME , PRIMARY KEY(ID))""")
		db.commit()
		print "logDateTime table is created"
	except: 
		print "Error: the datetime database is being rolled back"
		db.rollback()
#----------------------------------------------------------------------------------------------
def insertLogDateTime(db, startDate, startTime, endDate, endTime):
	curs = db.cursor()
   
	try:
		curs.execute("""INSERT INTO logDateTime (startDate, startTime, endDate, endTime) values(%s, %s, %s, %s)""", (startDate, startTime, endDate, endTime))   
		db.commit()
		print "SaveDateTime Data committed"

	except: 
		print "Error: the datetime database is being rolled back"
		db.rollback()
