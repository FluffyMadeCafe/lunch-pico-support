from machine import Pin, SPI
import gc9a01
import vga1_bold_16x32 as font

spi = SPI(1, baudrate=60000000, sck=Pin(14), mosi=Pin(15))
tft = gc9a01.GC9A01(
    spi,
    240,
    240,
    reset=Pin(11, Pin.OUT),
    cs=Pin(13, Pin.OUT),
    dc=Pin(12, Pin.OUT),
    backlight=Pin(10, Pin.OUT),
    rotation=0)

tft.init()
tft.fill(gc9a01.BLACK)
tft.text(font, "Hello.", 80, 100, gc9a01.RED)