import threading
import time
import Drawer
import os

debug = False

if not debug:
    from waveshare_epd import epd2in9_V2
    import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
    from gps import *
    epd = epd2in9_V2.EPD()

    epd.init()
    epd.Clear(0xFF)

shutdown_event = threading.Event()

delay_data = 1

def DataProcessing():

    return




def ClearScreen():
    print("Clearing the screen...")
    epd.init()
    time.sleep(1)
    epd.Clear(0xFF)
    time.sleep(1)


def task1():
    time_last_data = time.time() - delay_data

    while not shutdown_event.is_set():
        now = time.time()

        if(time_last_data + delay_data) < now:
            time_last_data = now

            DataProcessing()
    
    print("Shutting down...")

    img = Drawer.CreateNew(128,296)
    img = Drawer.ShutdownImage(img)
    img_new = img.rotate(90, expand=True)

    if not debug:
        epd.display(epd.getbuffer(img_new))

    time.sleep(3)
    ClearScreen()
    time.sleep(1)
    #os.system("sudo shutdown now -h") 

t1 = threading.Thread(target=task1)
t1.start()


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


def real_cb(channel):
    print("Button " + str(channel) + " was pushed!")
    
    if channel == 3:
        #PowerButton
        shutdown_event.set()
        return
    
    if channel == 4:
        #Function Button
        print("Done!")
        return

GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

cb1 = ButtonHandler(3, real_cb, edge='falling', bouncetime=10)
cb1.start()

cb2 = ButtonHandler(4, real_cb, edge='falling', bouncetime=10)
cb2.start()

GPIO.add_event_detect(3, GPIO.BOTH, callback=cb1)
GPIO.add_event_detect(4, GPIO.BOTH, callback=cb2)


while True:
    time.sleep(0.1)