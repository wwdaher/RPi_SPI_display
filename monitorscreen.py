# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import socket
from netifaces import interfaces, ifaddresses, AF_INET
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont, ImageColor
from adafruit_rgb_display import ili9341
from time import sleep
import psutil
import mygauges
import math
import busio
from xpt2046 import Touch
from gpiozero import Button, DigitalOutputDevice

# First define some constants to allow easy resizing of shapes.
BORDER = 20
FONTSIZE = 12

SCREENBACKGROUNDCOLOR = ImageColor.getrgb("salmon")
OBJBORDERCOLOR = ImageColor.getrgb("black")
OBJBACKGROUNDCOLOR = ImageColor.getrgb("lightsalmon")
GAUGEDIALCOLOR = ImageColor.getrgb("black")


#DEFAULTFONTLOCATION = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
#DEFAULTFONTLOCATION = "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf"
#DEFAULTFONTLOCATION = "/usr/share/fonts/truetype/freefont/FreeSans.ttf"
#DEFAULTFONTLOCATION = "/usr/share/fonts/truetype/freefont/FreeSerif.ttf"
#DEFAULTFONTLOCATION = "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"
#DEFAULTFONTLOCATION = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
#DEFAULTFONTLOCATION = "/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Regular.ttf"
#DEFAULTFONTLOCATION = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
#DEFAULTFONTLOCATION = "/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf"
#DEFAULTFONTLOCATION = "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"
#DEFAULTFONTLOCATION = "/usr/share/fonts/truetype/liberation2/LiberationSansNarrow-Regular.ttf"
#DEFAULTFONTLOCATION = "/usr/share/fonts/truetype/liberation2/LiberationSerif-Regular.ttf"
#DEFAULTFONTLOCATION = "/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf"
#DEFAULTFONTLOCATION = "/usr/share/fonts/truetype/piboto/Piboto-Regular.ttf"
#DEFAULTFONTLOCATION = "/usr/share/fonts/truetype/piboto/Piboto-Light.ttf"
DEFAULTFONTLOCATION = "/usr/share/fonts/truetype/quicksand/Quicksand-Regular.ttf"
DEFAULTFONT = ImageFont.truetype(DEFAULTFONTLOCATION, FONTSIZE)

def getIPData():
    IPAddr = socket.gethostbyname(hostname)

def getIPAddrs():
    IPAddrs = ""
    for ifaceName in interfaces():
        if (ifaceName != 'lo'):
            addresses = [
                i["addr"]
                for i in ifaddresses(ifaceName).setdefault(AF_INET, [{"addr": "No IP"}])
            ]
#            print(ifaceName + ": " + " ".join(addresses))
            IPAddrs += ifaceName + ": " + " ".join(addresses) + "\n"
    return IPAddrs[:-1]


# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# pylint: disable=line-too-long
# Create the display:
disp = ili9341.ILI9341(
    spi,
    rotation=180,  # 2.2", 2.4", 2.8", 3.2" ILI9341
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)
# pylint: enable=line-too-long

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
if disp.rotation % 180 == 90:
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
else:
    width = disp.width  # we swap height/width to rotate it to landscape!
    height = disp.height


#--------------------------------------------------------------
# now all the touch stuff
# add to /boot/firmware/config.txt: dtoverlay=spi1-1cs
#   connect cs cable to GPIO18, not 17 as code says
#these two need to be at the top
#   from xpt2046 import Touch
#   from gpiozero import Button, DigitalOutputDevice

# touch callback
def touchscreen_press(x, y):
    #calc based on screen orientation
    realx = x;
    realy = disp.height - y
    print(realx,realy)

#SCLK_1 (GPIO21) 	<--> 	CLK
#CE_1   (GPIO17)    <--> 	CS
#MOSI_1 (GPIO20) 	<--> 	DIN
#MISO_1 (GPIO19) 	<--> 	DO
#GPIO26 	        <--> 	IRQ
cs = DigitalOutputDevice(17)
clk = board.SCLK_1	# same as writing 21
mosi = board.MOSI_1	# same as writing 20
miso = board.MISO_1	# same as writing 19
irq = Button(26)


spi = busio.SPI(clk, mosi, miso)	# auxiliary SPI

xpt = Touch(spi, cs=cs, int_pin=irq, int_handler=touchscreen_press)
# end of touch stuff
#--------------------------------------------------------------

image = Image.new("RGB", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

#fill entire screen with background
draw.rectangle(xy = (0, 0, width, height),
               fill=SCREENBACKGROUNDCOLOR
               )
disp.image(image)


#display the host name
hostname = socket.gethostname()
mygauges.mytextbox(image=image,
                   topleft=(10,10),
                   bottomright=(230, 50),
                   text="Hostname: " + hostname,
                   backgroundcolor=OBJBACKGROUNDCOLOR,
                   bordercolor=OBJBORDERCOLOR,
                   textcolor=GAUGEDIALCOLOR,
                   fontloc=DEFAULTFONTLOCATION,
                   )

IPs = getIPAddrs()
mygauges.mytextbox(image=image,
                   topleft=(10,60),
                   bottomright=(230, 120),
                   text=IPs,
                   backgroundcolor=OBJBACKGROUNDCOLOR,
                   bordercolor=OBJBORDERCOLOR,
                   textcolor=GAUGEDIALCOLOR,
                   fontloc=DEFAULTFONTLOCATION,
                   )

while 1:
    virtualpercent = psutil.virtual_memory().percent 
    mygauges.mygauge(image=image, 
                     topleft=(10,130), 
                     bottomright=(115,180),
                     percent=virtualpercent ,
                     title="Virtual Memory" ,
                     text=str(virtualpercent)+"%" ,
                     backgroundcolor=OBJBACKGROUNDCOLOR,
                     dialcolor=ImageColor.getrgb("cyan"),
                     bordercolor=OBJBORDERCOLOR,
                     textcolor=GAUGEDIALCOLOR,
                     fontloc=DEFAULTFONTLOCATION,
                     outline=GAUGEDIALCOLOR,
                    )
    
    cpu_temp = psutil.sensors_temperatures()["cpu_thermal"][0]
    mygauges.mygauge(image=image, 
                     topleft=(125,130), 
                     bottomright=(230,180),
                     percent=math.trunc(cpu_temp.current),
                     text=str(math.trunc(cpu_temp.current))+"°C" ,
                     title="CPU Temp",
                     backgroundcolor=OBJBACKGROUNDCOLOR,
                     bordercolor=OBJBORDERCOLOR,
                     dialcolor=ImageColor.getrgb("orchid"),
                     fontloc=DEFAULTFONTLOCATION,
                     outline=GAUGEDIALCOLOR,
                     textcolor=GAUGEDIALCOLOR,
                    )
    
    cpupercent = psutil.cpu_percent(interval=1) 
    mygauges.mydial(image=image, 
                     topleft=(60,190), 
                     dialsize=120,
                     percent=cpupercent ,
                     text=str(cpupercent)+"%" ,
                     title="CPU",
                     backgroundcolor=OBJBACKGROUNDCOLOR,
                     bordercolor=OBJBORDERCOLOR,
                     textcolor=ImageColor.getrgb("green"),
                     fontloc=DEFAULTFONTLOCATION,
                     outline=ImageColor.getrgb("darkgreen"),
                    )


    sleep(1)

    disp.image(image)





for cpupercent in range(0, 101, 10):
    mygauges.mydial(image=image, 
                     topleft=(50,190), 
                     dialsize=120,
                     percent=cpupercent ,
                     text=str(cpupercent)+"%" ,
                     title="CPU",
                     backgroundcolor=OBJBACKGROUNDCOLOR,
                     bordercolor=OBJBORDERCOLOR,
                     textcolor=ImageColor.getrgb("green"),
                     fontloc=DEFAULTFONTLOCATION,
                     outline=ImageColor.getrgb("darkgreen"),
                    )
    sleep(1)
    disp.image(image)

