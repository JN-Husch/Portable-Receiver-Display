# 
# Content of individual pages
#

import Drawer
import subprocess
import Classes
import DataFetcher

font_large = 20
font_small = 20

###################################################
# Main Page showing ADSB Data
###################################################

def Page0(img,tgts,rate_avg,tgts_daily):
    img = Drawer.CreateText(img,10,5,"ADSB",font="ArialBold.ttf",sze=font_large)

    img = Drawer.CreateText(img,10,35,"Targets:",font="Arial.ttf",sze=font_large)
    img = Drawer.CreateText(img,10,55,str(len(tgts)),font="ArialBold.ttf",sze=font_small)
    
    img = Drawer.CreateText(img,10,80,"Rate:",font="Arial.ttf",sze=font_large)
    img = Drawer.CreateText(img,10,100,str(round(rate_avg)) + " /sec",font="ArialBold.ttf",sze=font_small)
    
    img = Drawer.CreateText(img,10,125,"Total:",font="Arial.ttf",sze=font_large)
    img = Drawer.CreateText(img,10,145,str(len(tgts_daily)),font="ArialBold.ttf",sze=font_small)

    max_range = "UNK"
    if len(tgts) > 0:
        max_range = str(round(tgts[0].dis / 1852,1)) + "NM"

    img = Drawer.CreateText(img,10,170,"Max Range:",font="Arial.ttf",sze=font_large)
    img = Drawer.CreateText(img,10,190,max_range,font="ArialBold.ttf",sze=font_small)

    return img

###################################################
# Page Showing an overview of the closest targets
###################################################

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

###################################################
# Page Showing an overview of the furthest targets
###################################################

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

###################################################
# GPS Information
###################################################

def Page3(img,gps_pos: Classes.Position3D,sat_cnt,sat_cnt_tot,time):
    img = Drawer.CreateText(img,10,5,"GPS",font="ArialBold.ttf",sze=font_large)

    lat_s = "No 2D Fix"
    if gps_pos.lat is not None and gps_pos.lat > -999:
        lat_s = str(round(gps_pos.lat,5)) + "°"

    img = Drawer.CreateText(img,10,35,"Lat:",font="Arial.ttf",sze=font_large)
    img = Drawer.CreateText(img,10,55,lat_s,font="ArialBold.ttf",sze=font_small)

    lng_s = "No 2D Fix"
    if gps_pos.lng is not None and gps_pos.lng > -999:
        lng_s = str(round(gps_pos.lng,5)) + "°"

    img = Drawer.CreateText(img,10,80,"Lon:",font="Arial.ttf",sze=font_large)
    img = Drawer.CreateText(img,10,100,lng_s,font="ArialBold.ttf",sze=font_small)


    alt_string = "No 3D Fix"
    if gps_pos.alt is not None and gps_pos.alt > -999:
        try:
            alt_string = str(round(gps_pos.alt)) + "m"
        except:
            alt_string = "UKN"

    img = Drawer.CreateText(img,10,125,"Alt:",font="Arial.ttf",sze=font_large)
    img = Drawer.CreateText(img,10,145,alt_string,font="ArialBold.ttf",sze=font_small)

    img = Drawer.CreateText(img,10,170,"Sats:",font="Arial.ttf",sze=font_large)
    img = Drawer.CreateText(img,10,190,str(sat_cnt) + "/" + str(sat_cnt_tot),font="ArialBold.ttf",sze=font_small)

    img = Drawer.CreateText(img,10,215,"Time:",font="Arial.ttf",sze=font_large)
    img = Drawer.CreateText(img,10,235,str(time),font="ArialBold.ttf",sze=font_small)
    return img

###################################################
# Information and Settings
###################################################

def Page4(img,gain_adj):
    img = Drawer.CreateText(img,10,5,"Network",font="ArialBold.ttf",sze=font_large)

    wifi = subprocess.check_output(['sudo', 'iwgetid']).decode().split("ESSID:")[1].replace("\"","")

    img = Drawer.CreateText(img,10,35,"WiFi:",font="Arial.ttf",sze=font_large)    
    img = Drawer.CreateText(img,10,55,wifi,font="ArialBold.ttf",sze=15)

    res = str(subprocess.check_output(['hostname', '-I'])).split(' ')[0].replace("b'", "")

    img = Drawer.CreateText(img,10,80,"IP:",font="Arial.ttf",sze=font_large)    
    img = Drawer.CreateText(img,10,100,res,font="ArialBold.ttf",sze=15)

    img = Drawer.CreateText(img,10,140,"Receiver",font="ArialBold.ttf",sze=font_large)
    img = Drawer.CreateText(img,10,170,"Gain:",font="Arial.ttf",sze=font_large)    
    img = Drawer.CreateText(img,10,190,DataFetcher.getGain(),font="ArialBold.ttf",sze=font_small)
    
    if gain_adj:
        img = Drawer.CreateRectangle(img,10,215,108,50)
        img = Drawer.CreateText(img,10,220,"  Adjusting",font="Arial.ttf",sze=font_small,col="#FFFFFF")    
        img = Drawer.CreateText(img,10,240,"    gain...",font="Arial.ttf",sze=font_small,col="#FFFFFF")    
    else:
        img = Drawer.CreateText(img,10,210,"Hold F button for",font="Arial.ttf",sze=15)    
        img = Drawer.CreateText(img,10,230,"1s for automatic",font="Arial.ttf",sze=15)    
        img = Drawer.CreateText(img,10,250,"gain adjustment!",font="Arial.ttf",sze=15)    

    return img

###################################################
# Page Selection Function
###################################################

def PageSelector(img,page_no, use_gps):
    if page_no == 0:
        img = Drawer.CreateRectangle(img,5,275,15,19)
        img = Drawer.CreateText(img,8,275,("1"),font="ArialBold.ttf",sze=18,col="#FFFFFF")
    else:
        img = Drawer.CreateText(img,8,275,("1"),font="Arial.ttf",sze=18)

    if page_no == 1:
        img = Drawer.CreateRectangle(img,30,275,15,19)
        img = Drawer.CreateText(img,33,275,("2"),font="ArialBold.ttf",sze=18,col="#FFFFFF")
    else:
        img = Drawer.CreateText(img,33,275,("2"),font="Arial.ttf",sze=18)

    if page_no == 2:
        img = Drawer.CreateRectangle(img,55,275,15,19)
        img = Drawer.CreateText(img,58,275,("3"),font="ArialBold.ttf",sze=18,col="#FFFFFF")
    else:
        img = Drawer.CreateText(img,58,275,("3"),font="Arial.ttf",sze=18)

    if page_no == 3:
        img = Drawer.CreateRectangle(img,80,275,15,19)
        if use_gps:
            img = Drawer.CreateText(img,83,275,("4"),font="ArialBold.ttf",sze=18,col="#FFFFFF")
    else:
        if use_gps:
            img = Drawer.CreateText(img,83,275,("4"),font="Arial.ttf",sze=18)    
    
    if page_no == 4:
        img = Drawer.CreateRectangle(img,105,275,15,19)
        if use_gps:
            img = Drawer.CreateText(img,108,275,("5"),font="ArialBold.ttf",sze=18,col="#FFFFFF")
        else:
            img = Drawer.CreateText(img,108,275,("4"),font="ArialBold.ttf",sze=18,col="#FFFFFF")        
    else:
        if use_gps:
            img = Drawer.CreateText(img,108,275,("5"),font="Arial.ttf",sze=18)
        else:
            img = Drawer.CreateText(img,108,275,("4"),font="Arial.ttf",sze=18)

    return img