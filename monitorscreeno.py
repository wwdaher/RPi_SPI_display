#---------------------------------------------------------------------
# monitorscreeno: object oriented version of a performance monitor
# 		  screen for a raspberry pi running a 2.4" TFT
# 		  at 320x240
# 		  Config file monitorscreeno.ini must be present
#
#		  GPL license applies
#
# author: 
# 	wdaher
# version:
# 	0.0	2024/11/01
#	1.0	2024/12/03	add monitorscreeno.ini support
# 	
#---------------------------------------------------------------------
import socket
from netifaces import interfaces, ifaddresses, AF_INET
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageShow
from adafruit_rgb_display import ili9341
from time import sleep, time_ns
import psutil
import mygauges
import math
import busio
from xpt2046 import Touch
from gpiozero import Button, DigitalOutputDevice
from mygaugeso import Bar, TextBox, Dial, Gauge, BarMulti
from random import randrange
import configparser
import sys

#---------------------------------------------------------------------
# read the config file
#---------------------------------------------------------------------
config = configparser.ConfigParser()
config.read('monitorscreeno.ini')
SCREENBACKGROUNDCOLOR = ImageColor.getrgb(config['default']['screenbackgroundcolor'])
try:
	SCREENBACKGROUNDIMAGE = config['default']['screenbackgroundimage']
except:
	SCREENBACKGROUNDIMAGE = ''
OBJBORDERCOLOR = ImageColor.getrgb(config['default']['objbordercolor'])
OBJBACKGROUNDCOLOR = ImageColor.getrgb(config['default']['objbackgroundcolor'])
GAUGEDIALCOLOR = ImageColor.getrgb(config['default']['gaugedialcolor'])

UPDATEFREQUENCY = int(config['default']['updatefrequency'])
DEFAULTFONTLOCATION = config['default']['fontlocation']
FONTSIZE = int(config['default']['fontsize'])

NET_MAXBYTES_PER_SECOND = int(config['default']['net_maxbytes_per_second'])     # 30Mb/sec
DISK_MAXBYTES_PER_SECOND = int(config['default']['disk_maxbytes_per_second'])     # 30Mb/sec


BAUDRATE = int(config['default']['screen_baudrate'])

#---------------------------------------------------------------------
# set up default font
#---------------------------------------------------------------------
DEFAULTFONT = ImageFont.truetype(DEFAULTFONTLOCATION, FONTSIZE)

#---------------------------------------------------------------------
# get information about network adapters and addresses
#---------------------------------------------------------------------
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
            IPAddrs += ifaceName + ": " + " ".join(addresses) + ", "
    return IPAddrs[:-2]

#---------------------------------------------------------------------
# calculate disk and network activityi
#---------------------------------------------------------------------
prev_net_bytes = 0
prev_net_time = time_ns()
prev_disk_bytes = 0
net_percent = 0
disk_percent = 0
def calcIO():
    global prev_net_bytes, prev_disk_bytes, prev_net_time, net_percent, disk_percent
    global NET_MAXBYTES_PER_SECOND, DISK_MAXBYTES_PER_SECOND
    now = time_ns()
    elapsed = (now - prev_net_time) / 1000000000  # in seconds
#    print("elapsed: " + str(elapsed))
    prev_net_time = now
    net_bytes = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
    net_rw = net_bytes - prev_net_bytes
    prev_net_bytes = net_bytes

    net_percent = int(((net_rw / elapsed) / NET_MAXBYTES_PER_SECOND ) * 100)
    if net_percent > 100:
        net_percent = 100

    disk_bytes = psutil.disk_io_counters().read_bytes + psutil.disk_io_counters().write_bytes
#    print( psutil.disk_io_counters().read_bytes,  psutil.disk_io_counters().write_bytes)
    disk_rw = disk_bytes - prev_disk_bytes
    prev_disk_bytes = disk_bytes

    disk_percent = int(((disk_rw / elapsed) / DISK_MAXBYTES_PER_SECOND) * 100)
    if disk_percent > 100:
        disk_percent = 100

#    print('net : ' + str(net_rw) + '  disk : ' + str(disk_rw))
#    print('net %: ' + str(net_percent) + '  disk %: ' + str(disk_percent))




#---------------------------------------------------------------------
# configure details about the screen and how its connected
#---------------------------------------------------------------------
# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

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


#---------------------------------------------------------------------
# now all the touch stuff
#---------------------------------------------------------------------
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
#---------------------------------------------------------------------
# end of touch stuff
#---------------------------------------------------------------------

#---------------------------------------------------------------------

#fill entire screen with background
#image = Image.open('roundlines.png')
if SCREENBACKGROUNDIMAGE != '':
	image = Image.open(SCREENBACKGROUNDIMAGE)
	disp.image(image)
else:

	image = Image.new("RGBA", (width, height))
	# Get drawing object to draw on image.
	draw = ImageDraw.Draw(image)

	draw.rectangle(xy = (0, 0, width, height),
               fill=SCREENBACKGROUNDCOLOR
               )

#---------------------------------------------------------------------
# divide the screen into two small, two medium and one large row
#---------------------------------------------------------------------
rowcount = 5
rowtop = [0]*rowcount
rowbottom = [0]*rowcount
rowleftmargin = 10
rowleftright = 115
rowrightmargin = 125
rowrightright = 230
rowspace = 10
rowheight = [0]*5
rowheight[0] = 30
rowheight[1] = 30
rowheight[2] = 55
rowheight[3] = 50
rowheight[4] = 105
rowtop[0] = 5
rowbottom[0] = rowtop[0] + rowheight[0]
for i in range(1, 5):
    rowtop[i] = rowtop[i-1] + rowheight[i-1] + rowspace
    rowbottom[i] = rowtop[i] + rowheight[i]

#---------------------------------------------------------------------
# display the host name
#---------------------------------------------------------------------
hostname = socket.gethostname()
hostnametb = TextBox(image, (rowleftmargin,rowtop[0]), (rowrightright, rowbottom[0]))
hostnametb.set_text("Hostname: " + hostname)
hostnametb.set_background_color(OBJBACKGROUNDCOLOR)
hostnametb.set_border_color(OBJBORDERCOLOR)
hostnametb.set_text_color(GAUGEDIALCOLOR)
hostnametb.set_font_loc(DEFAULTFONTLOCATION)
hostnametb.refresh()

#---------------------------------------------------------------------
# textbox with the IP addresses
#---------------------------------------------------------------------
IPs = getIPAddrs()
iptb = TextBox(image, (rowleftmargin,rowtop[1]), (rowrightright, rowbottom[1]))
iptb.set_text(IPs)
iptb.set_background_color(OBJBACKGROUNDCOLOR)
iptb.set_border_color(OBJBORDERCOLOR)
iptb.set_text_color(GAUGEDIALCOLOR)
iptb.set_font_loc(DEFAULTFONTLOCATION)
iptb.set_font_size(16)
iptb.refresh()

#---------------------------------------------------------------------
# Bargraph with network and disk activity
#---------------------------------------------------------------------
iobc = BarMulti(image,(rowleftmargin, rowtop[2]), (rowrightright, rowbottom[2]), 2)
iobc.set_title("I/O")
iobc.set_title_color(ImageColor.getrgb('black'))
iobc.set_background_color(OBJBACKGROUNDCOLOR)
#iobc.set_dial_color(ImageColor.getrgb("purple"))
iobc.set_border_color(OBJBORDERCOLOR)
iobc.set_text_color(ImageColor.getrgb("white"))
iobc.set_text(("Network", 'Disk'))
iobc.set_font_loc(DEFAULTFONTLOCATION)
iobc.set_outline(ImageColor.getrgb("darkgreen"))
iobc.set_gradient_colors(ImageColor.getrgb("pink"), ImageColor.getrgb("purple"))
iobc.set_gradient(True)
iobc.set_barempty_color(ImageColor.getrgb("lightslategray"))

#---------------------------------------------------------------------
# gauge wtih the amount of virtual memory used
#---------------------------------------------------------------------
perg = Gauge(image,(rowleftmargin,rowtop[3]), (rowleftright,rowbottom[3]))
perg.set_title("Virtual Memory")
perg.set_background_color(OBJBACKGROUNDCOLOR)
perg.set_dial_color(ImageColor.getrgb("cyan"))
perg.set_border_color(OBJBORDERCOLOR)
perg.set_text_color(GAUGEDIALCOLOR)
perg.set_font_loc(DEFAULTFONTLOCATION)
perg.set_outline(GAUGEDIALCOLOR)
perg.set_dialempty_color(ImageColor.getrgb("lightslategray"))



#---------------------------------------------------------------------
# gauge wtih CPU temperatur
#---------------------------------------------------------------------
tempg = Gauge(image,(rowrightmargin,rowtop[3]), (rowrightright,rowbottom[3]))
tempg.set_title("CPU Temp")
tempg.set_background_color(OBJBACKGROUNDCOLOR)
tempg.set_dial_color(ImageColor.getrgb("orchid"))
tempg.set_border_color(OBJBORDERCOLOR)
tempg.set_text_color(GAUGEDIALCOLOR)
tempg.set_font_loc(DEFAULTFONTLOCATION)
tempg.set_outline(GAUGEDIALCOLOR)
tempg.set_dialempty_color(ImageColor.getrgb("lightslategray"))


#---------------------------------------------------------------------
# dial for total CPU activity
#---------------------------------------------------------------------
cpud = Dial(image,(rowleftmargin, rowtop[4]), 105)
cpud.set_title("CPU")
cpud.set_background_color(OBJBACKGROUNDCOLOR)
cpud.set_dial_color(ImageColor.getrgb("purple"))
cpud.set_border_color(OBJBORDERCOLOR)
cpud.set_text_color(ImageColor.getrgb("green"))
cpud.set_font_loc(DEFAULTFONTLOCATION)
cpud.set_outline(ImageColor.getrgb("darkgreen"))
cpud.set_gradient_colors(ImageColor.getrgb("yellow"), ImageColor.getrgb("red"))
cpud.set_gradient(True)
cpud.set_dialempty_color(ImageColor.getrgb("lightslategray"))

#---------------------------------------------------------------------
# bargraph with activity for individual CPU cores
#---------------------------------------------------------------------
cpur = BarMulti(image,(rowrightmargin, rowtop[4]), (rowrightright, rowbottom[4]), 4)
cpur.set_title("CPU Cores")
cpur.set_title_color(ImageColor.getrgb('black'))
cpur.set_background_color(OBJBACKGROUNDCOLOR)
#cpur.set_dial_color(ImageColor.getrgb("purple"))
cpur.set_border_color(OBJBORDERCOLOR)
cpur.set_text_color(ImageColor.getrgb("white"))
cpur.set_text(("I", 'II', 'III', 'IV'))
cpur.set_font_loc(DEFAULTFONTLOCATION)
cpur.set_outline(ImageColor.getrgb("darkgreen"))
cpur.set_graph_outline_color(ImageColor.getrgb("darkblue"))
cpur.set_gradient_colors(ImageColor.getrgb("lightgreen"), ImageColor.getrgb("black"))
cpur.set_gradient(True)
cpur.set_barempty_color(ImageColor.getrgb("lightslategray"))

#---------------------------------------------------------------------
# now loop forever, each time displaying updated values
#---------------------------------------------------------------------

while 1:

    virtualpercent = psutil.virtual_memory().percent 
    perg.set_percent(virtualpercent)
    perg.set_text(str(virtualpercent) + '%')

    cpu_temp = psutil.sensors_temperatures()["cpu_thermal"][0]
    tempg.set_percent(math.trunc(cpu_temp.current))
    tempg.set_text(str(math.trunc(cpu_temp.current))+"°C")

    calcIO()
    iobc.set_percent((net_percent, disk_percent))

    cpupercent = psutil.cpu_percent(interval=UPDATEFREQUENCY) 
    cpud.set_percent(cpupercent)
    cpud.set_text(str(cpupercent)+"%")

    rawcpumpercent = psutil.cpu_percent(interval=UPDATEFREQUENCY, percpu=True)
    cpumpercent = ()
    for i in range(0, len(rawcpumpercent)):  
        cpumpercent = cpumpercent + (int(rawcpumpercent[i]),)
    cpur.set_percent(cpumpercent)
    image.putalpha(28)
    disp.image(image)

    sleep(UPDATEFREQUENCY)



#---------------------------------------------------------------------
# following code only for testing purposes
#---------------------------------------------------------------------


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

