#!/usr/bin/env python
import MySQLdb

def connect():
    db = MySQLdb.connect('localhost', 'root', 'raspberry', 'logs')
    if db is None:
        print("Error: Unable to connect to the database")
    return db
#--------------------------------------------------------------------------------------------
def createRawTable(db):
	curs = db.cursor()

	try:
		curs.execute("""USE logs""")
		curs.execute("""DROP TABLE IF EXISTS rawEX""")
		curs.execute("""CREATE TABLE rawEX(date DATE, time TIME, lat float, longitude float,
			alt float, speed float, temp float, aX float, aY float, aZ float, cX float, cY float, cZ float, gyX float, gyY float, gyZ float)""")
		db.commit()
		print "rawEX table is created"
	except: 
		print "Error: the database is being rolled back"
		db.rollback()

#-----------------------------------------------------------------------------------------------
def insertRawEX(db, date, time, lat, longitude, alt, speed, temp, aX, aY, aZ, cX, cY, cZ, gyX, gyY, gyZ):
	curs = db.cursor()

	try:
		curs.execute("""INSERT INTO rawEX 
         	  values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (date, time, lat, longitude, alt, speed, temp, aX, aY, aZ, cX, cY, cZ, gyX, gyY, gyZ))   
		#insert_str = "INSERT INTO %s" % (table)
		#print insert_str
		#middle_str = " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % (date, time, lat, longitude, alt, speed, temp, gyX, gyY, gyZ, compass)
		#print middle_str
		#final_str = insert_str + middle_str
		
		#final_str = "INSERT INTO %s" % (table) + " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % (date, time, lat, longitude, alt, speed, temp, gyX, gyY, gyZ, compass)
		#print "HERE?"
		#print "final: " + final_str
		#curs.execute(final_str)
		db.commit()
		print "Data committed"

	except: 
		print "Error: the database is being rolled back"
		db.rollback()
#-------------------------------------------------------------------------------------
def getRawEX(db):
	curs = db.cursor()

	curs.execute("SELECT * FROM rawEX")
	#curs.execute("SELECT TOP 5 * FROM rawEX")
	print "\nDate\tTime\tLat\tLong\tAlt\tSpeed\tTemp\tgyX\tgyY\tgyZ\tcompass"
	print "========================================================================================="

	for row in curs.fetchall():
		date = str(row[0])
		time = str(row[1])
		lat = str(row[2])
		lon = str(row[3])
		alt = str(row[4])
		speed = str(row[5])
		temp = str(row[6])
		aX = str(row[7])
		aY = str(row[8])
		aZ = str(row[9])
		cX = str(row[10])
		cY = str(row[11])
		cZ = str(row[12])
		gyX = str(row[13])
		gyY = str(row[14])
		gyZ = str(row[15])
		
		print "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % \
			(date, time, lat, lon, alt, speed, temp, aX, aY, aZ, cX, cY, cZ, gyX, gyY, gyZ)
#---------------------------------------------------------------------------------------------------
def createProcessedTable(db):
	curs = db.cursor()

	try:
		curs.execute("""USE logs""")
		curs.execute("""DROP TABLE IF EXISTS processed""")
		curs.execute("""CREATE TABLE processed(date DATE, time TIME, lat float, longitude float,
			alt float, speed float, temp float, gyX float, gyY float, gyZ float, compass float)""")
		db.commit()
		print "processed table is created"
	except: 
		print "Error: the database is being rolled back"
		db.rollback()
#----------------------------------------------------------------------------------------------
def insertProcessed(db, date, time, lat, longitude, alt, speed, temp, gyX, gyY, gyZ, compass):
	curs = db.cursor()
   
	try:
		curs.execute("""INSERT INTO processed
           values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (date, time, lat, longitude, alt, speed, temp, gyX, gyY, gyZ, compass))   
		db.commit()
		print "Data committed"

	except: 
		print "Error: the database is being rolled back"
		db.rollback()
#--------------------------------------------------------------------------------------------
def createSaveTable(db):
	curs = db.cursor()

	try:
		curs.execute("""USE logs""")
		curs.execute("""DROP TABLE IF EXISTS saving""")
		curs.execute("""CREATE TABLE saving(date DATE, time TIME, lat float, longitude float,
			alt float, speed float, temp float, aX float, aY float, aZ float, cX float, cY float, cZ float, gyX float, gyY float, gyZ float)""")
		db.commit()
		print "saving table is created"
	except: 
		print "Error: the database is being rolled back"
		db.rollback()
#----------------------------------------------------------------------------------------------
def insertSaving(db, date, time, lat, longitude, alt, speed, temp, gyX, gyY, gyZ, compass):
	curs = db.cursor()
   
	try:
		curs.execute("""INSERT INTO saving
           values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (date, time, lat, longitude, alt, speed, temp, gyX, gyY, gyZ, compass))   
		db.commit()
		print "Data committed"

	except: 
		print "Error: the database is being rolled back"
		db.rollback()
