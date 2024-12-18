# RPi_SPI_display
Python code for SPI display for Raspberry Pi

This turns a standard 2.4" TFT 320x240 display into a system activity
monitor for a Raspberry Pi. Testing was done with "2.4 TFT SPI 240*320 V1.2", "JC2432S024". The STL file to print a front panel to hold this display and fits into the Fractal Designs North Pi case is also included.

## Hardware
- print the Fractal Designs case
- modify the case so that the wires connecting the screen can reach over the top fan and be attached to the GPIO pins (a Dremel tool is handy)
- print the front insert
- install the screen into the insert. The fit is very tight, so install the screen diagonally and then strighten it out
- attach the wires to the screen, then pass them through over the top fan into the case
- connect all the wires to the GPIO pins

## Software

This code requires the adafruit_rgb_display library with the ili9341 driver. Touch requires the xpt2046 library. Drawing is with the PIL library.

The activity driver program is monitorscreen.py, and it requires the graphicobjects library. The library code to implement the various graph objects is in graphicobjects.py. The objects in graphicobjects.py
are not tied to the display monitor and can be used in any other application.

Ensure that SPI is enabled in raspi-config.

## Install Instructions
- sudo pip3 install Adafruit-blinka
- sudo pip3 install netifaces
- sudo pip3 install adafruit-circuitpython-rgb-display
- git clone https://github.com/ilbertt/XPT2046-Python.git
- copy xpt2046.py into working directory from XPT2046-Python created in previous step
#### if running on a Raspberry Pi 5, do the following:
The libraries for RPi seem to be in flux as I had to try various combinations of this to get it to work on different RPi
machines even though they were fresh builds.
- sudo apt remove python3-rpi.gpio
- sudo apt remove RPi.GPIO
- pip3 install rpi-lgpio
- add dtoverlay=spi0-0cs to /boot/firmware/config.txt

## Pin Connection Configuration

### Display connection
|Screen |GPIO | RPi pin |
|-------|-----|---------|
|VCC | 5VO | 2 |
|GND | GND | 6 |
|CS | GPIO8 (CEO) | 24 |
|RESET | GPIO24 | 18 |
|D/C | GPIO25 | 22 |
|SDI (MOSI) | GPIO10 (MOSI) | 19 |
|SCK | GPIO11 (SCLK) | 23 |
|LED | GPIO27 | 13 |
|SDO(MISO) | GPIO9 (MISO) | 21 |

### Touch functionality:
Add the following to /boot/firmware/config.txt: 

`dtoverlay=spi1-1cs`

|Screen |GPIO | RPi pin |
|-------|-----|---------|
|T_CLK | GPIO21 | 40 |
|T_CS | GPIO18 | 12 |
|T_DIN | GPIO20 | 38 |
|T_DO | GPIO19 | 35 | 
|T_IRQ | GPIO26 | 37 |


