from machine import Pin, I2C, RTC
import time
from ds3231_port import DS3231

sda = Pin(16)
scl = Pin(17)
i2c = I2C(0, sda=sda, scl=scl, freq=400000)

RTC_time = RTC()
RTC_time.datetime((1976,2,27,4,10,20,30,0))
DS3231_time = DS3231(i2c)
DS3231_time.save_time()
    
while True:
    TIME = DS3231_time.get_time()
    
    date_result = str(TIME[0]) + '/' + str(TIME[1]) + '/' + str(TIME[2])
    time_result = str(TIME[3]) + ':' + str(TIME[4]) + ':' + str(TIME[5])

    print(date_result)
    print(time_result)

    time.sleep(1)