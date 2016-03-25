#!/usr/bin/env python
import MySQLdb

def connect():
    db = MySQLdb.connect('localhost', 'main', 'password', 'logs')
    if db is None:
        print("Error: Unable to connect to the database")
    return db

#curs = connect()
#if curs:
#    print "hello"
#else:
#    print "its me"
