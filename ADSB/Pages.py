# 
# Content of individual pages
#

import Drawer
import subprocess

font_large = 20
font_small = 20

def Page0(img,tgts,rate_avg,tgts_daily):
    img = Drawer.CreateText(img,10,5,"ADSB",font="ArialBold.ttf",sze=font_large)

    img = Drawer.CreateText(img,10,35,"Targets:",font="Arial.ttf",sze=font_large)
    img = Drawer.CreateText(img,10,55,str(len(tgts)),font="ArialBold.ttf",sze=font_small)
    
    img = Drawer.CreateText(img,10,80,"Rate:",font="Arial.ttf",sze=font_large)
    img = Drawer.CreateText(img,10,100,str(round(rate_avg)) + " /sec",font="ArialBold.ttf",sze=font_small)
    
    img = Drawer.CreateText(img,10,125,"Total:",font="Arial.ttf",sze=font_large)
    img = Drawer.CreateText(img,10,145,str(len(tgts_daily)),font="ArialBold.ttf",sze=font_small)


    return img

def Page1(img,tgts):
    img = Drawer.CreateText(img,10,5,"Closest",font="ArialBold.ttf",sze=font_large)

    length = len(tgts)

    if length > 5:
        length = 5
    
    for i in range(0,length):
        img = Drawer.CreateText(img,10,35 + i * 48,tgts[i].flt,font="ArialBold.ttf",sze=16)

        dis = round(tgts[i].dis / 1852,1)

        img = Drawer.CreateText(img,10,55 + i * 48,str(dis) + "NM",font="Arial.ttf",sze=16)



    return img

def Page2(img,tgts):
    img = Drawer.CreateText(img,10,5,"Furthest",font="ArialBold.ttf",sze=font_large)

    length = len(tgts)

    if length > 5:
        length = 5
    
    for i in range(0,length):
        img = Drawer.CreateText(img,10,35 + i * 48,tgts[i].flt,font="ArialBold.ttf",sze=16)

        dis = round(tgts[i].dis / 1852,1)

        img = Drawer.CreateText(img,10,55 + i * 48,str(dis) + "NM",font="Arial.ttf",sze=16)

    return img

def Page3(img,lat,lng,alt,sat_cnt,sat_cnt_tot,time):
    img = Drawer.CreateText(img,10,5,"GPS",font="ArialBold.ttf",sze=font_large)

    lat_s = "No 2D Fix"
    if lat is not None:
        lat_s = str(round(lat,5)) + "°"

    img = Drawer.CreateText(img,10,35,"Lat:",font="Arial.ttf",sze=font_large)
    img = Drawer.CreateText(img,10,55,lat_s,font="ArialBold.ttf",sze=font_small)

    lng_s = "No 2D Fix"
    if lng is not None:
        lng_s = str(round(lng,5)) + "°"

    img = Drawer.CreateText(img,10,80,"Lon:",font="Arial.ttf",sze=font_large)
    img = Drawer.CreateText(img,10,100,lng_s,font="ArialBold.ttf",sze=font_small)


    alt_string = "No 3D Fix"
    if alt is not None:
        try:
            alt_string = str(round(alt)) + "m"
        except:
            alt_string = "UKN"

    img = Drawer.CreateText(img,10,125,"Alt:",font="Arial.ttf",sze=font_large)
    img = Drawer.CreateText(img,10,145,alt_string,font="ArialBold.ttf",sze=font_small)

    img = Drawer.CreateText(img,10,170,"Sats:",font="Arial.ttf",sze=font_large)
    img = Drawer.CreateText(img,10,190,str(sat_cnt) + "/" + str(sat_cnt_tot),font="ArialBold.ttf",sze=font_small)

    img = Drawer.CreateText(img,10,215,"Time:",font="Arial.ttf",sze=font_large)
    img = Drawer.CreateText(img,10,235,str(time),font="ArialBold.ttf",sze=font_small)
    return img

def Page4(img):
    img = Drawer.CreateText(img,10,5,"Network",font="ArialBold.ttf",sze=font_large)

    wifi = subprocess.check_output(['sudo', 'iwgetid']).decode().split("ESSID:")[1].replace("\"","")

    img = Drawer.CreateText(img,10,35,"WiFi:",font="Arial.ttf",sze=font_large)    
    img = Drawer.CreateText(img,10,55,wifi,font="ArialBold.ttf",sze=15)

    res = str(subprocess.check_output(['hostname', '-I'])).split(' ')[0].replace("b'", "")

    img = Drawer.CreateText(img,10,80,"IP:",font="Arial.ttf",sze=font_large)    
    img = Drawer.CreateText(img,10,100,res,font="ArialBold.ttf",sze=15)

    return img

def Page5(img):
    img = Drawer.CreateText(img,10,5,"Info",font="ArialBold.ttf",sze=font_large)

    wifi = subprocess.check_output(['sudo', 'iwgetid']).decode().split("ESSID:")[1].replace("\"","")

    img = Drawer.CreateText(img,10,35,"WiFi:",font="Arial.ttf",sze=font_large)    
    img = Drawer.CreateText(img,10,60,wifi,font="ArialBold.ttf",sze=15)

    res = str(subprocess.check_output(['hostname', '-I'])).split(' ')[0].replace("b'", "")

    img = Drawer.CreateText(img,10,95,"IP:",font="Arial.ttf",sze=font_large)    
    img = Drawer.CreateText(img,10,120,res,font="ArialBold.ttf",sze=15)

    return img