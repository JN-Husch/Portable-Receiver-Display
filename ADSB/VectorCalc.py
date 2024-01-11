#
# Mathematical Calculations for relative target position
#

import math
import Classes

#Returns the 2D Distance in m
def DisCalc2D(lat_tgt,lng_tgt,homePos:Classes.Position3D):
    
    d_lat = (lat_tgt - homePos.lat) * 60
    d_lng = (lng_tgt - homePos.lng) * 60 * math.cos(homePos.lat * math.pi / 180)

    d_lat = d_lat * 1852
    d_lng = d_lng * 1852

    dis_2D = math.sqrt(d_lat*d_lat + d_lng*d_lng)
    return dis_2D

#Return: 0: 3D Distance in m, 1: Azimuth in °, 2: Ele in °
def AngleCalc(alt_tgt, lat_tgt, lng_tgt,  homePos: Classes.Position3D):
    if lat_tgt == -999 or lng_tgt == -999:
        return [-999,-999,-999]

    d_alt = alt_tgt * 0.3048 #ALT in Meters
    d_alt = d_alt - homePos.alt

    d_lat = (lat_tgt - homePos.lat) * 60
    d_lng = (lng_tgt - homePos.lng) * 60 * math.cos(homePos.lat * math.pi / 180)

    d_lat = d_lat * 1852
    d_lng = d_lng * 1852

    dis_2D = math.sqrt(d_lat*d_lat + d_lng*d_lng)
    dis_3D = math.sqrt(dis_2D*dis_2D + d_alt*d_alt)

    ele = 90 - math.acos(d_alt / dis_3D) * 180 / math.pi
    azi = math.acos(d_lat / dis_2D) * 180 / math.pi

    if d_lng < 0:
        azi = 360 - azi

    return [dis_3D, azi, ele]
