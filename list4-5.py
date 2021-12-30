from machine import Pin, UART
import time
from micropyGPS import MicropyGPS

gps_module = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

TIMEZONE = 9
my_gps = MicropyGPS(TIMEZONE)

count = 0

while True:
    length = gps_module.any()
    
    if length > 0:
        b = gps_module.read(length)
        for x in b:
            msg = my_gps.update(chr(x))
    
    t = my_gps.timestamp

    gpsTime = '{:02d}:{:02d}:{:02d}'.format(t[0], t[1], int(t[2]))
    
    d = my_gps.date

    gpsDate = '{:02d}/{:02d}/{:02d}'.format(d[2], d[1], d[0])
    
    print(count)
    print('Time:', gpsTime)
    print('Date:', gpsDate)
    
    time.sleep_ms(3000)
    
    count = count + 1