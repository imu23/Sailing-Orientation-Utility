#!/usr/bin/python
import time
from time import sleep
start = 0
while True:
    f = open('timelog', 'w')
    time = time.time()
    s = str(start)
    f.write(str(time))
    f.write('\t')
    f.write(s)
    f.write('\n')
    sleep(600)
    start = start + 600
