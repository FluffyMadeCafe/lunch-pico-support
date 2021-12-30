from machine import Pin, SPI
import gc9a01
import vga1_bold_16x32 as font
import gc
import os
import sdcard

gc.enable()
gc.collect()

spi1 = SPI(1, baudrate=60000000, sck=Pin(14), mosi=Pin(15))
spi0 = SPI(0)
sd = sdcard.SDCard(spi0, Pin(28))
os.mount(sd, '/sd')
os.chdir('sd')
    
tft = gc9a01.GC9A01(
    spi1,
    240,
    240,
    reset=Pin(11, Pin.OUT),
    cs=Pin(13, Pin.OUT),
    dc=Pin(12, Pin.OUT),
    backlight=Pin(10, Pin.OUT),
    rotation=0)

tft.init()
    
tft.jpg('/sd/bluemarble.jpg', 0, 0, gc9a01.SLOW)

tft.text(font, "Hello.", 80, 100, gc9a01.RED)