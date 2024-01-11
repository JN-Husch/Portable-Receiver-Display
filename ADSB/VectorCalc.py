import math
import Classes

delta_time = 0.1  #value in seconds

def calcPred(tgt: Classes.Aircraft, homePos: Classes.HomePosition):

    tgtPred = []
    time = tgt.time

    if tgt.spd is not None and tgt.spd < 999 and tgt.trk is not None and tgt.trk < 999:

        for a in range(0,100,1):
            timeFuture = round(time + a * delta_time,3)

            #Distance = Speed in m/s * Steps * Time

            spd = tgt.spd * 1852 / 60 / 60    #kt to m/s

            delta_dis2D = round(spd * a * delta_time,2)

            delta_dis2D = delta_dis2D / 1852        #Convert to N/M

            trk = tgt.trk * math.pi / 180

            #Distance 1D

            delta_LAT = delta_dis2D * math.cos(trk) / 60

            delta_LNG = delta_dis2D * math.sin(trk) / 60 / math.cos(tgt.lat * math.pi / 180)

            trk = trk * 180 / math.pi

            if False and trk > 90 and trk < 270:
                delta_LAT = delta_LAT * -1

            if trk > 180 and trk < 360:
                delta_LNG = delta_LNG * 1

            lat = tgt.lat + delta_LAT
            lng = tgt.lng + delta_LNG

            angles = AngleCalc(tgt.alt,lat,lng,homePos)

            tgtPred.append([timeFuture,angles[1],angles[2],angles[0]])

    return tgtPred

#Returns the 2D Distance in m
def DisCalc2D(lat_tgt,lng_tgt,homePos:Classes.HomePosition):
    
    d_lat = (lat_tgt - homePos.lat) * 60
    d_lng = (lng_tgt - homePos.lng) * 60 * math.cos(homePos.lat * math.pi / 180)

    d_lat = d_lat * 1852
    d_lng = d_lng * 1852

    dis_2D = math.sqrt(d_lat*d_lat + d_lng*d_lng)
    return dis_2D

#Return: 0: 3D Distance in m, 1: Azimuth in °, 2: Ele in °
def AngleCalc(alt_tgt, lat_tgt, lng_tgt,  homePos: Classes.HomePosition):
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
