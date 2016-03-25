## Process some extra things based on pressure
#	EHH
import math

def getAltitude(press, sealevel_pa=101325.0):
    alt = 44330.0 * (1.0 - pow(press / sealevel_pa, (1.0/5.255)))
    return alt
    
def getSealevelPress(press, alt=0.0):
    p = press / pow(1.0 - alt/44330.0, 5.255)
    return p
