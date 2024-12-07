# RPi_SPI_display
Python code for SPI display for Raspberry Pi

This turns a standard 2.4" TFT 320x240 display into a system activity
monitor for a Raspberry Pi. Testing was done with "2.4 TFT SPI 240*320 V1.2", "JC2432S024"

This code requires the adafruit_rgb_display library with the ili9341 driver. Touch requires the xpt2046 library. Drawing is with the PIL library.

The core driver is monitorscreeno.py. The code to implement the various graph objects is in mygaugeso.py.

Ensure that SPI is enabled in raspi-config.

## Install Instructions
- sudo pip3 install Adafruit-blinka
- sudo pip3 install netifaces
- sudo pip3 install adafruit-circuitpython-rgb-display
- git clone https://github.com/ilbertt/XPT2046-Python.git
- copy xpt2046.py into working directory from XPT2046-Python created in previous step
if running on a Raspberry Pi 5, do the following:
- sudo apt remove python3-rpi.gpio
- pip3 install rpi-lgpi

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
|LED | 3.5V power | 1 |
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


