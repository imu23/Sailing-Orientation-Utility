#!/usr/bin/env python

from dbLink import *



#try:
#    curs.execute ("""INSERT INTO rawEX 
#            values('2015-09-04', NOW(), '43.7686', '40.452', '13.453', '5.05', '24.5', '34.454', '56.324', '56.234', '14.343')""")
     
#    db.commit()
#    print "Data committed"

#except: 
#	print "Error: the database is being rolled back"
#	db.rollback()

db = connect()
createRawTable(db)
table = "rawEx"
insertRawEX(db, table, '2016-05-06', '18:45:00', '96.434', '89.546', '26.040', '1.05', '100.00', '14.533', '13.943', '12.003', '1.000')
#getRawEX(db)




#curs = db.cursor()

#curs.execute("SELECT * FROM rawEX")
#space = 't'
#print "\nDate\tTime\tLat\tLong\tAlt\tSpeed\tTemp\tgyX\tgyY\tgyZ\tcompass"
#print "========================================================================================="


#for row in curs.fetchall():
#	date = str(row[0])
#	time = str(row[1])
#	lat = str(row[2])
#	lon = str(row[3])
#	alt = str(row[4])
#	speed = str(row[5])
#	temp = str(row[6])
#	gyX = str(row[7])
#	gyY = str(row[8])
#	gyZ = str(row[9])
#	compass = str(row[10])
	
#	print "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % \
#		(date, time, lat, lon, alt, speed, temp, gyX, gyY, gyZ, compass)
	

