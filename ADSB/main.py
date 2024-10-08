#
# Main Program Loop
#

import threading
import time
from time import sleep
import DataFetcher
import VectorCalc
import Classes
import Drawer
import Pages
import operator
import os
from gpiozero import Button
from signal import pause
import json

from dateutil import parser
from datetime import datetime, timedelta
from PIL import Image,ImageDraw,ImageFont
from waveshare_epd import epd2in9_V2


####################################################################################
#
# ---------------------- USER ADJUSTABLE SETTINGS BELOW ----------------------------
#
####################################################################################

url = "http://127.0.0.1/tar1090/data/aircraft.json" # Path to aircraft.json
delay_data = 1                                  # Refresh rate for data in seconds

# Home Position (used if there is no GPS module or no GPS Signal)
home_pos = Classes.Position3D()
home_pos.lat = 0                    # Home Latitude
home_pos.lng = 0                    # Home Longitude
home_pos.alt = 0                    # Home Altitude in m

use_gps = True                      # Variable if a GPS receiver is available

####################################################################################
#
# ---------------------- END OF USER ADJUSTABLE SETTINGS ---------------------------
#
####################################################################################

# Page Setup
page_no = 0                         # Active Page Number
page_max = 4                        # Total Count of available Pages (starting at 0)
page_timer = 0                      # Variable for return to page 0 function


# Receiver Position
rec_pos = Classes.Position3D()

# GPS Position
gps_pos = Classes.Position3D()

# Stats
tgts_daily = []
msgs_prev = 0
rate_avg = 0

# Variables
sat_cnt = 0                         # Used GPS Satellite Count
sat_cnt_tot = 0                     # Total GPS Satellite Count
sat_time = 0                        # Time from GPS
sat_gdop = 0                        # GDOP (3D + Time Accuracy) from GPS

flash = False                       # Flash Variable used for flashing activity corner
adjusting_gain = False              # Flag for Gain Adjust Process Initiated

# Events for Threading
shutdown_event = threading.Event()
clearscreen_event = threading.Event()

###################################################
# Begin of Program Initialization
###################################################

# GPS Initialization
try:
    from gps3 import gps3
    print("GPS3 Pip Package found")
    gps_socket = gps3.GPSDSocket()
    data_stream = gps3.DataStream()
    gps_socket.connect()
    gps_socket.watch()
except ModuleNotFoundError:
    print("No GPS3 Pip Package found")
    use_gps = False
    rec_pos = home_pos


# E-Ink Display Initalization
epd = epd2in9_V2.EPD()
epd.init()
epd.Clear(0xFF)

img = Drawer.CreateNew(epd.width,epd.height)    # Creating a empty image (128x296)
img_new = img.rotate(90, expand=True)           # Rotating empty image for vertical screen orientation

epd.display_Base(epd.getbuffer(img_new))        # Display empty image on E-Ink Display


def DataProcessing():
    global tgts
    global msgs_prev
    global tgts_daily
    global rate_avg
    global flash
    global rec_pos
    global use_gps
    global gps_pos
    global sat_cnt
    global sat_cnt_tot
    global sat_time
    global adjusting_gain

    #if use_gps:
    #    getPositionData()

    tgts = DataFetcher.fetchADSBData(url)  

    if tgts is None:
        return

    for tgt in tgts:
        tgt.dis = VectorCalc.AngleCalc(tgt.alt,tgt.lat,tgt.lng,rec_pos)[0]


        if(tgt.hex not in tgts_daily):
            tgts_daily.append(tgt.hex)

    tgts_close = sorted(tgts, key=operator.attrgetter('dis'))
    tgts_far = sorted(tgts, key=operator.attrgetter('dis'),reverse=True)

    tgts_close_filt = []
    for tgt in tgts_close:
        if tgt.dis != -999:
            tgts_close_filt.append(tgt)
    
    tgts_close = tgts_close_filt


    #Calculate Message Rate
    msg_rate = 0

    if (len(tgts) > 0):
        if(msgs_prev != 0):
            msg_rate = (tgts[0].msgs - msgs_prev) / delay_data

        msgs_prev = tgts[0].msgs
    
    rate_avg = msg_rate * 0.2 + rate_avg * 0.8

    #img = Drawer.CreateNew(epd.width,epd.height)
    img = Drawer.CreateNew(128,296)

    if flash:
        Drawer.CreateRectangle(img,123,0,5,5) 
    
    flash = not flash

    img = Drawer.CreateRectangle(img,0,272,128,1)

    # Select which page to draw
    if page_no == 0:
        img = Pages.Page0(img,tgts_far,rate_avg,tgts_daily)
    elif page_no == 1:
        img = Pages.Page1(img,tgts_close)
    elif page_no == 2:
        img = Pages.Page2(img,tgts_far)
    elif page_no == 3:
        img = Pages.Page3(img,gps_pos,sat_cnt,sat_cnt_tot,sat_time,sat_gdop)
    elif page_no == 4:
        img = Pages.Page4(img,adjusting_gain)

    img = Pages.PageSelector(img,page_no, use_gps)               # Draw Page Selector at the bottom
    img_new = img.rotate(90, expand=True)               # Rotate image to fit vertical screen
    epd.display_Partial(epd.getbuffer(img_new))         # Do a partial update of E-Ink Display


def ClearScreen():
    print("Clearing the screen...")
    epd.init()
    time.sleep(1)
    epd.Clear(0xFF)
    time.sleep(1)

# Main Task for Data Processing
def task1():
    # Main Loop triggered every second
    time_last_data = time.time() - delay_data

    while not shutdown_event.is_set():
        # Hold Thread in program loop
        now = time.time()

        if(time_last_data + delay_data) < now:
            time_last_data = now

        if clearscreen_event.is_set():      # Clear Screen event does a clear screen
            ClearScreen()
            clearscreen_event.clear()       # Reset Clear Screen event

        DataProcessing()

    ###################################################
    # Shutdown Routine:
    ###################################################
        
    print("Shutting down...")

    # Display Shutdown image on E-Ink Display:
    img = Drawer.CreateNew(128,296)
    img = Drawer.ShutdownImage(img)
    img_new = img.rotate(90, expand=True)
    epd.display(epd.getbuffer(img_new))

    time.sleep(3)
    ClearScreen()                           # Clearing the screen before commencing shutdown
    time.sleep(1)
    os.system("sudo shutdown now -h")       # Sending the shutdown command to the OS

# Secondary Task for GPS Interface
def task2():
    while not shutdown_event.is_set():
        getPositionData()
        time.sleep(0.1)

# Optional Task to automatically adjust gain every 2 minutes - Currently not called
def task3():
    print("Automatically adjusting gain...")
    os.system("sudo autogain1090") 
    print("Done!")

# Clear Stats
def Clear():
    global tgts_daily
    tgts_daily.clear()
    tgts_daily = []

def getPositionData():
    global use_gps

    if not use_gps:
        return
    
    global rec_pos
    global home_pos
    global gps_pos
    global sat_cnt
    global sat_cnt_tot
    global sat_time
    global sat_gdop

    sats = []

    for new_data in gps_socket:
        if new_data:
            data_stream.unpack(new_data)
            lat_s = data_stream.TPV['lat']
            lng_s = data_stream.TPV['lon']
            alt_s = data_stream.TPV['alt']

            gps_pos = Classes.Position3D()

            if lat_s is not None and lat_s != "n/a":
                gps_pos.lat = float(data_stream.TPV['lat'])

            if lng_s is not None and lng_s != "n/a":
                gps_pos.lng = float(data_stream.TPV['lon'])
            
            if alt_s is not None and alt_s != "n/a":
                gps_pos.alt = float(data_stream.TPV['alt'])

            # Find out if GPS Position is available
            if gps_pos.lat != -999 and gps_pos.lng != -999:
                # 2D Position available
                rec_pos.lat = gps_pos.lat
                rec_pos.lng = gps_pos.lng
                
                if gps_pos.alt != -999:
                    # 3D Postion available
                    rec_pos.alt = gps_pos.alt
                else:
                    # 2D Postion only - set altitude to 0m
                    rec_pos.alt = 0
            else:
                # No GPS Position available, set receiver position to home position
                rec_pos = home_pos

            # Get Time and Date from GPS
            gps_time = data_stream.TPV['time']
            date = 0
            sat_time = 0

            if(gps_time is not None and len(gps_time) > 10):
                date = parser.parse(gps_time)
                sat_time = date.strftime("%H:%M:%S") + "Z"

            sat_gdop = data_stream.SKY['gdop']

            # Get a List of GPS Sats and count the used vs total numbers
            sats =  data_stream.SKY['satellites']

            sat_cnt = 0
            sat_cnt_tot = 0

            if sats == "n/a":
                break

            for sat in sats:
                sat_cnt_tot = sat_cnt_tot + 1

                if sat['used']:
                    sat_cnt = sat_cnt + 1


button_pwr = Button(3, bounce_time=0.1)
button_fnc = Button(4, bounce_time=0.1)

timer_fnc = 0


def pwr_btn_mom():
    # Power Button Momentarily   
    global shutdown_event
    shutdown_event.set()


def fnc_btn_rise():
    global timer_fnc
    timer_fnc = time.time()


def fnc_btn_fall():
    # Function Button Handler
    global page_no, use_gps, adjusting_gain, timer_fnc
       
    if (time.time() - timer_fnc) < 1:
        #Short Press
        page_no = page_no + 1
            
        # If GPS is not used, skip GPS page
        if not use_gps and page_no == 3:
            page_no = page_no + 1

        # If page is larger than maximum number of pages, reset to 0
        if page_no > page_max:
            page_no = 0
            clearscreen_event.set()


def fnc_btn_held():
    # Function Button Handler
    global page_no, use_gps, adjusting_gain, timer_fnc
       
    if (time.time() - timer_fnc) > 1:
        #Long Press
        if page_no == 4:
            # On Page 4, use Long Press to adjust Gain
            adjusting_gain = True
            os.system("sudo autogain1090")
            time.sleep(3)
            adjusting_gain = False
        else:
            # On all other pages, reset page to 0, without screen refresh
            page_no = 0 


button_pwr.when_pressed = pwr_btn_mom
button_fnc.when_pressed = fnc_btn_rise
button_fnc.when_released = fnc_btn_fall
button_fnc.when_held = fnc_btn_held

#t1 - Main Thread for data processing
t1 = threading.Thread(target=task1)
t1.start()

#t2 - Secondary Thread for GPS interface
if use_gps:
    t2 = threading.Thread(target=task2)
    t2.start()

while True:
    time.sleep(0.1)