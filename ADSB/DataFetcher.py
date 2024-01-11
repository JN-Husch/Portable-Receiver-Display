#
# Data loading from aircraf.json
#

import json
import Classes

from contextlib import closing
from urllib.request import Request, urlopen


def fetchADSBData(url):
    request_site = Request(url, headers={"User-Agent": "Mozilla/5.0"})

    tgts = []
    try:
        with closing(urlopen(request_site)) as aircraft_file:
            aircraft_data = json.load(aircraft_file)
    except:
        print("An exception occurred while trying to fetch aircraft.json") 
        return


    for a in aircraft_data["aircraft"]:
        timestmp = aircraft_data.get("now")

        tgt = Classes.Aircraft()

        tgt.hex = a.get("hex")
        tgt.lat = a.get("lat")
        tgt.lng = a.get("lon")
        tgt.flt = a.get("flight")
        tgt.alt = a.get("alt_geom")
        tgt.spd = a.get("gs")
        tgt.trk = a.get("track")
        tgt.msgs = aircraft_data.get("messages")

        seen_pos = a.get("seen_pos")

        #Some cleanup to prevent invalid variables being passed on:
        if tgt.reg is None or len(tgt.reg) < 1:
            tgt.reg = tgt.hex

        if tgt.flt is None:
            tgt.flt = tgt.reg

        if tgt.swk is None:
            tgt.swk = 9999

        if tgt.alt is None:
            tgt.alt = -999
        
        if tgt.spd is None:
            tgt.spd = -999

        if tgt.trk is None:
            tgt.trk = -999

        if tgt.lat is None:
            tgt.lat = -999        
        
        if tgt.lng is None:
            tgt.lng = -999    

        if seen_pos is None:
            seen_pos = 0

        tgt.time = timestmp - seen_pos

        tgts.append(tgt)

    return tgts


