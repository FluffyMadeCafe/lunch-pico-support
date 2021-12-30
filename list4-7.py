"""
main.py
    Pico Pin: 36 (3V3 OUT) is V（＋）.
    Pico Pin: 38（GND） is V（−）.
    
    LCD connected to a Raspberry Pi Pico.
    Pico Pin   LCD
    =========  ====
    20 (GP15)  DIN
    19 (GP14)  CLK
    17 (GP13)  CS
    16 (GP12)  DC
    15 (GP11)  RST
    14 (GP10)  BL
        
    Micro SD Card module connected to a Raspberry Pi Pico.
    Pico Pin   Micro SD Card module
    =========  ====================
    34 (GP28)  CS
    10 (GP7)   DI
    6 (GP4)    DO
    9 (GP6)    CLK
    
    GPS module connected to a Raspberry Pi Pico.
    Pico Pin   GPS module
    =========  ==========
    1 (GP0)    RXD
    21(GP1)    TXD
    
    RTC module connected to a Raspberry Pi Pico.
    Pico Pin   RTC module
    =========  ==========
    22 (GP17)  SCL
    21 (GP16)  SDA
    
    switch connected to a Raspberry Pi Pico.
    Pico Pin   switch
    =========  ==========
    29 (GP22)  PULL_UP
"""
# import from default library
from machine import Pin, SPI, UART, I2C, RTC
import gc, os, time

# import library for LCD
import gc9a01
import vga1_bold_16x32 as font

# import library for Micro SD Card
import sdcard

# import library for GPS
from micropyGPS import MicropyGPS

# import library for RTC
from ds3231_port import DS3231

# switch init
led = Pin(25, Pin.OUT)
switch = Pin(22, Pin.IN, Pin.PULL_UP)

# gc init
gc.enable()
gc.collect()

# LCD init
spi1 = SPI(1, baudrate=60000000, sck=Pin(14), mosi=Pin(15))  
tft = gc9a01.GC9A01(
    spi1,
    240,
    240,
    reset=Pin(11, Pin.OUT),
    cs=Pin(13, Pin.OUT),
    dc=Pin(12, Pin.OUT),
    backlight=Pin(10, Pin.OUT),
    rotation=0)

# Micro SD Card init
spi0 = SPI(0)
sd = sdcard.SDCard(spi0, Pin(28))
os.mount(sd, '/sd')
os.chdir('sd')

# GPS init
gps_module = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
TIMEZONE = 9
my_gps = MicropyGPS(TIMEZONE)

# RTC init
sda = Pin(16)
scl = Pin(17)
i2c = I2C(0, sda=sda, scl=scl, freq=400000)

# GPS_fix function
def GPS_fix():
    # clear screen
    tft.init()
    # paint black
    tft.fill(gc9a01.BLACK)
    while True:
        # LED status
        led.value(0)
        # getting data from GPS
        length = gps_module.any()
            
        if length > 0:
            b = gps_module.read(length)
            for x in b:
                msg = my_gps.update(chr(x))
            
        t = my_gps.timestamp
        fixTime = '{:02d}:{:02d}:{:02d}'.format(t[0], t[1], int(t[2]))
        d = my_gps.date 
        if (int(t[0]) >= 0) and (int(t[0]) < 9):
            day = d[0] + 1
        else:
            day = d[0]
        fixDate = '{:02d}/{:02d}/{:02d}'.format(d[2], d[1], day)
        # draw Date and Time
        tft.text(font, "Fix now ...", 50, 50, gc9a01.WHITE)
        tft.text(font, fixDate, 50, 100, gc9a01.WHITE)
        tft.text(font, fixTime, 50, 150, gc9a01.WHITE)
        # break process for switch
        if (switch.value() == 0):
            # set Date and Time
            RTC_time = RTC()
            year = 2000 + int(d[2])
            RTC_time.datetime((year, d[1], day, 0, t[0], t[1], int(t[2]), 0))
            DS3231_time = DS3231(i2c)
            DS3231_time.save_time()
            # LED status
            led.value(1)
            break
        time.sleep(1)

# clear screen
tft.init()
# draw jpg
tft.jpg('/sd/bluemarble.jpg', 0, 0, gc9a01.SLOW)

while True:
    # LED status
    led.value(0)
    if switch.value() == 0:
        GPS_fix()
        # clear screen
        tft.init()
        # draw jpg
        tft.jpg('/sd/bluemarble.jpg', 0, 0, gc9a01.SLOW)
    # getting data from RTC
    DS3231_time = DS3231(i2c)
    TIME = DS3231_time.get_time()
    gpsDate = '{:0>2}/{:0>2}/{:0>2}'.format(str(TIME[0]), str(TIME[1]), str(TIME[2]))
    gpsTime = '{:0>2}:{:0>2}:{:0>2}'.format(str(TIME[3]), str(TIME[4]), str(TIME[5]))
    # draw Date and Time
    tft.text(font, "GPS Time", 50, 50, gc9a01.WHITE)
    tft.text(font, gpsDate, 30, 100, gc9a01.WHITE)
    tft.text(font, gpsTime, 50, 150, gc9a01.WHITE)
    
    time.sleep(1)