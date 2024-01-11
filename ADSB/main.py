import threading
import time
import DataFetcher
import VectorCalc
import Classes
import Drawer
import Pages
import operator
import schedule
import os
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

from dateutil import parser
from datetime import datetime, timedelta
from PIL import Image,ImageDraw,ImageFont
from waveshare_epd import epd2in9_V2

from gps3 import gps3
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()


page_no = 3
page_max = 4


epd = epd2in9_V2.EPD()
epd.init()
epd.Clear(0xFF)

#img = Drawer.CreateNew(epd.width,epd.height)
img = Drawer.CreateNew(128,296)
img_new = img.rotate(90, expand=True)


epd.display_Base(epd.getbuffer(img_new))

delay_data = 2

url = "http://127.0.0.1/tar1090/data/aircraft.json"

#Kloten
home = Classes.HomePosition()
home.lat = 47.4448839
home.lng = 8.58839802
home.alt = 495

tgts_daily = []
msgs_prev = 0
rate_avg = 0

#gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)

sat_cnt = 0
sat_cnt_tot = 0
lat = 0
lng = 0
alt = 0
sat_time = 0

shutdown_event = threading.Event()
clearscreen_event = threading.Event()


def getPositionData2():
    global gpsd
    global lat
    global lng
    global alt
    global sat_cnt
    global sat_cnt_tot
    global sat_time

    gpsd.read()
    gpsd.read()
    gpsd.read()

    lat = gpsd.fix.latitude
    lng = gpsd.fix.longitude
    alt = gpsd.fix.altitude
    sat_cnt = gpsd.satellites_used
    sat_cnt_tot = len(gpsd.satellites)
    gps_time = gpsd.utc
    

    date = 0
    sat_time = 0

    if(gps_time is not None and len(gps_time) > 10):
        date = parser.parse(gps_time)
        sat_time = date.strftime("%H:%M:%S") + "Z"

def getPositionData():
    global gpsd
    global lat
    global lng
    global alt
    global sat_cnt
    global sat_cnt_tot
    global sat_time

    sats = []

    for new_data in gps_socket:
        if new_data:
            data_stream.unpack(new_data)
            lat_s = data_stream.TPV['lat']
            lng_s = data_stream.TPV['lon']
            alt_s = data_stream.TPV['alt']

            if lat_s is not None and lat_s != "n/a":
                lat = float(data_stream.TPV['lat'])
            
            if lng_s is not None and lng_s != "n/a":
                lng = float(data_stream.TPV['lon'])
            
            if alt_s is not None and alt_s != "n/a":
                alt = float(data_stream.TPV['alt'])

            gps_time = data_stream.TPV['time']
            date = 0
            sat_time = 0

            if(gps_time is not None and len(gps_time) > 10):
                date = parser.parse(gps_time)
                sat_time = date.strftime("%H:%M:%S") + "Z"

            sats =  data_stream.SKY['satellites']

            sat_cnt = 0
            sat_cnt_tot = 0

            if sats == "n/a":
                return

            for sat in sats:
                sat_cnt_tot = sat_cnt_tot + 1

                if sat['used']:
                    sat_cnt = sat_cnt + 1
            #print(str(sat_cnt) + "/" + str(sat_cnt_tot))
            return

flash = False

def DataProcessing():
    global tgts
    global msgs_prev
    global tgts_daily
    global rate_avg
    global flash
    global lat
    global lng
    global alt
    global sat_cnt
    global sat_cnt_tot

    getPositionData()

    global sat_time

    tgts = DataFetcher.fetchADSBData(url)  

    if tgts is None:
        return

    for tgt in tgts:
        tgt.dis = VectorCalc.AngleCalc(tgt.alt,tgt.lat,tgt.lng,home)[0]


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

    if page_no == 0:
        img = Pages.Page0(img,tgts,rate_avg,tgts_daily)
        img = Drawer.CreateRectangle(img,5,275,15,19)
        img = Drawer.CreateText(img,8,275,("1").format(a = page_no, b = page_max),font="ArialBold.ttf",sze=18,col="#FFFFFF")
        img = Drawer.CreateText(img,33,275,("2").format(a = page_no, b = page_max),font="Arial.ttf",sze=18)
        img = Drawer.CreateText(img,58,275,("3").format(a = page_no, b = page_max),font="Arial.ttf",sze=18)
        img = Drawer.CreateText(img,83,275,("4").format(a = page_no, b = page_max),font="Arial.ttf",sze=18)
        img = Drawer.CreateText(img,108,275,("5").format(a = page_no, b = page_max),font="Arial.ttf",sze=18)

    elif page_no == 1:
        img = Pages.Page1(img,tgts_close)
        img = Drawer.CreateRectangle(img,30,275,15,19)
        img = Drawer.CreateText(img,8,275,("1").format(a = page_no, b = page_max),font="Arial.ttf",sze=18)
        img = Drawer.CreateText(img,33,275,("2").format(a = page_no, b = page_max),font="ArialBold.ttf",sze=18,col="#FFFFFF")
        img = Drawer.CreateText(img,58,275,("3").format(a = page_no, b = page_max),font="Arial.ttf",sze=18)
        img = Drawer.CreateText(img,83,275,("4").format(a = page_no, b = page_max),font="Arial.ttf",sze=18)
        img = Drawer.CreateText(img,108,275,("5").format(a = page_no, b = page_max),font="Arial.ttf",sze=18)

    elif page_no == 2:
        img = Pages.Page2(img,tgts_far)
        img = Drawer.CreateRectangle(img,55,275,15,19)
        img = Drawer.CreateText(img,8,275,("1").format(a = page_no, b = page_max),font="Arial.ttf",sze=18)
        img = Drawer.CreateText(img,33,275,("2").format(a = page_no, b = page_max),font="Arial.ttf",sze=18)
        img = Drawer.CreateText(img,58,275,("3").format(a = page_no, b = page_max),font="ArialBold.ttf",sze=18,col="#FFFFFF")
        img = Drawer.CreateText(img,83,275,("4").format(a = page_no, b = page_max),font="Arial.ttf",sze=18)
        img = Drawer.CreateText(img,108,275,("5").format(a = page_no, b = page_max),font="Arial.ttf",sze=18)

    elif page_no == 3:
        img = Pages.Page3(img,lat,lng,alt,sat_cnt,sat_cnt_tot,sat_time)
        img = Drawer.CreateRectangle(img,80,275,15,19)
        img = Drawer.CreateText(img,8,275,("1").format(a = page_no, b = page_max),font="Arial.ttf",sze=18)
        img = Drawer.CreateText(img,33,275,("2").format(a = page_no, b = page_max),font="Arial.ttf",sze=18)
        img = Drawer.CreateText(img,58,275,("3").format(a = page_no, b = page_max),font="Arial.ttf",sze=18)
        img = Drawer.CreateText(img,83,275,("4").format(a = page_no, b = page_max),font="ArialBold.ttf",sze=18,col="#FFFFFF")
        img = Drawer.CreateText(img,108,275,("5").format(a = page_no, b = page_max),font="Arial.ttf",sze=18)

    elif page_no == 4:
        img = Pages.Page4(img)
        img = Drawer.CreateRectangle(img,105,275,15,19)
        img = Drawer.CreateText(img,8,275,("1").format(a = page_no, b = page_max),font="Arial.ttf",sze=18)
        img = Drawer.CreateText(img,33,275,("2").format(a = page_no, b = page_max),font="Arial.ttf",sze=18)
        img = Drawer.CreateText(img,58,275,("3").format(a = page_no, b = page_max),font="Arial.ttf",sze=18)
        img = Drawer.CreateText(img,83,275,("4").format(a = page_no, b = page_max),font="Arial.ttf",sze=18)
        img = Drawer.CreateText(img,108,275,("5").format(a = page_no, b = page_max),font="ArialBold.ttf",sze=18,col="#FFFFFF")

    img_new = img.rotate(90, expand=True)

    epd.display_Partial(epd.getbuffer(img_new))


def ClearScreen():
    print("Clearing the screen...")
    epd.init()
    time.sleep(1)
    epd.Clear(0xFF)
    time.sleep(1)

def task1():
    #time_last_data = time.time() - delay_data

    while not shutdown_event.is_set():
        now = time.time()

        if clearscreen_event.is_set():
            ClearScreen()
            clearscreen_event.clear()

        if True or (time_last_data + delay_data) < now:
            time_last_data = now

            DataProcessing()

    print("Shutting down...")

    img = Drawer.CreateNew(128,296)
    img = Drawer.ShutdownImage(img)
    img_new = img.rotate(90, expand=True)

    epd.display(epd.getbuffer(img_new))

    time.sleep(3)
    ClearScreen()
    time.sleep(1)
    os.system("sudo shutdown now -h") 

#t1 = threading.Thread(target=task1)


def Clear():
    global tgts_daily
    tgts_daily.clear()
    tgts_daily = []

class ButtonHandler(threading.Thread):
    def __init__(self, pin, func, edge='both', bouncetime=200):
        super().__init__(daemon=True)

        self.edge = edge
        self.func = func
        self.pin = pin
        self.bouncetime = float(bouncetime)/1000

        self.lastpinval = GPIO.input(self.pin)
        self.lock = threading.Lock()

    def __call__(self, *args):
        if not self.lock.acquire(blocking=False):
            return

        t = threading.Timer(self.bouncetime, self.read, args=args)
        t.start()

    def read(self, *args):
        pinval = GPIO.input(self.pin)

        if (
                ((pinval == 0 and self.lastpinval == 1) and
                 (self.edge in ['falling', 'both'])) or
                ((pinval == 1 and self.lastpinval == 0) and
                 (self.edge in ['rising', 'both']))
        ):
            self.func(*args)

        self.lastpinval = pinval
        self.lock.release()

page_timer = 0

def real_cb(channel):
    global page_no
    global page_timer

    if channel == 3:
        #PowerButton
        print("Button " + str(channel) + " pressed!")
        shutdown_event.set()
        return
    
    if channel == 4:
        #Function Button
        #clearscreen_event.set()
        #print("Automatically adjusting gain...")
        #os.system("sudo autogain1090") 
        #print("Done!")

        if GPIO.input(4):
            #falling
            print("Button " + str(channel) + " released!")
            
            if time.time() - page_timer > 0.5:
                page_no = 0 
                return 
            
            page_no = page_no + 1
            
            if page_no > page_max:
                page_no = 0
                clearscreen_event.set()
        
            print("Page: " + str(page_no))   

        else:
            #rising
            print("Button " + str(channel) + " pressed!")
            page_timer = time.time()

        return
    
    

GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

cb1 = ButtonHandler(3, real_cb, edge='falling', bouncetime=10)
cb1.start()

cb2 = ButtonHandler(4, real_cb, edge='both', bouncetime=10)
cb2.start()


GPIO.add_event_detect(3, GPIO.BOTH, callback=cb1)
GPIO.add_event_detect(4, GPIO.BOTH, callback=cb2)

print("Starting schedules...")
#schedule.every().day.at("00:05").do(Clear)
schedule.every(1).seconds.do(task1())
#schedule.every(1).seconds.do(getPositionData(gpsd))

while True:
    schedule.run_pending()
    #getPositionData(gpsd)
    time.sleep(0.1)