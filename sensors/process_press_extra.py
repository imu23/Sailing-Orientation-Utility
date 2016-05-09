## Process some extra things based on pressure

import math

def getAltitude(press, sealevel_pa=101325.0):
    sl = getSealevelPress(press)
    alt = 44330.0 * (1.0 - pow(press / sl, (1.0/5.255)))
    #print "alt: ", alt
    return alt
    
def getSealevelPress(press, alt=0.0):
    p = press / pow(1.0 - alt/44330.0, 5.255)
    #print "sl: ", p
    return p
