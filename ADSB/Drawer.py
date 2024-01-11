#
#  Drawing functions using Pillow
#

import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

def CreateNew(w,h):
    shape = [(0, 0), (w, h)] 
  
    img = Image.new("RGB", (w, h)) 
    img1 = ImageDraw.Draw(img)   
    img1.rectangle(shape, fill ="#ffffff") 

    return img

def CreateRectangle(img, x,y,w,h,col = "#000000"):
    img1 = ImageDraw.Draw(img)
    
    shape = [(x, y), (x+w, y+h)] 
    img1.rectangle(shape, fill =col) 
    return img

def CreateText(img, x,y, txt,col = "#000000",sze = 25,font="CourierNew.ttf",opa=1.0):  
    absolute_path = os.path.dirname(__file__)
    mf = ImageFont.truetype(absolute_path + "/res/" + font, sze)

    img1 = ImageDraw.Draw(img)
    
    img1.text((x,y), txt, fill=col, font=mf) 
    return img

def ShutdownImage(img):
    img = CreateText(img,5,10,"Device is",font="Arial.ttf",sze=20)
    img = CreateText(img,5,35,"shuting off...",font="Arial.ttf",sze=20)
    img = CreateText(img,5,60,"PLEASE",font="ArialBold.ttf",sze=20)
    img = CreateText(img,5,85,"WAIT!",font="ArialBold.ttf",sze=20)
    img = CreateText(img,5,296 - 120,"Portable",font="ArialBold.ttf",sze=20)
    img = CreateText(img,5,296 - 95,"Receiver",font="ArialBold.ttf",sze=20)
    img = CreateText(img,5,296 - 70,"Software",font="ArialBold.ttf",sze=20)
    img = CreateText(img,5,296 - 45,"by JN-Husch",font="Arial.ttf",sze=20)
    img = CreateText(img,5,296 - 20,"Version: 1.0.0",font="Arial.ttf",sze=15)
    
    return img   