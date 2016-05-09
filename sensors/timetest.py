import dataFormat
import string
import gpsPoll
import time

gps = gpsPoll.GpsPoller()
t0 = gps.getTime()
count = 0
while t0 == "":
	print "count: ", count
	print "t0: ", t0
	gps.getNext()
	t0 = gps.getTime()
	time.sleep(.5)
	count = count + 1
	
print "count: ", count
print "t0: ", t0
	
t1 = "00:00:00"
t2 = "10:10:10"
t3 = "22:23:24"
t4 = "01:01:01"
t5 = "08:45:33"

t10 = dataFormat.convertTime("am/pm", "EDT", t0)
t11 = dataFormat.convertTime("am/pm", "EDT", t1)
t12 = dataFormat.convertTime("am/pm", "EDT", t2)
t13 = dataFormat.convertTime("am/pm", "EDT", t3)
t14 = dataFormat.convertTime("am/pm", "EDT", t4)
t15 = dataFormat.convertTime("am/pm", "EDT", t5)

print "t0: ", t10
print "t1: ", t11
print "t2: ", t12
print "t3: ", t13
print "t4: ", t14
print "t5: ", t15
