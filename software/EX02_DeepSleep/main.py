import os
import time
from machine import Pin, I2S, SDCard, SoftI2C, ADC, deepsleep, Timer, RTC, deepsleep
from bme680 import *
import i2smic
import RGBLib 

# LED CONTROLLER
LED = RGBLib.Controller(4,26,27)


#MIC LOADING
_MIC = i2smic.Controller()
_AUDIO_LENGTH = 15  #record audio for 15s
_READINGS_INTERVAL = 5 #collect 3 samples (_AUDIO_LENGTH//_READINGS_INTERVAL)
_SLEEP_TIME = 300  #deep sleep for 5min (300s)

# LDR SENSOR (ANALOGIC INTERFACE)
adc = ADC(Pin(34))
_MAXL = 65535

# BMP680 SENSOR (I2C INTERFACE)
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
bme = BME680_I2C(i2c=i2c)

# SDCARD MODULE (SPI INTERFACE)
sd = SDCard(slot=2)  # sck=18, mosi=23, miso=19, cs=5
os.mount(sd, "/sd")

#LOADING NEXT FILE: record_N
FCount = 1
FPath="/sd/record_{}.wav"
try:
    while os.stat(FPath.format(FCount)):
        FCount+=1
except:pass
print("New file:",FPath.format(FCount))
_AUDIO_FILE=FPath.format(FCount)
_LOG_FILE = "/sd/data.log"
_SLEEP_TIME = 120 #Seconds

# REAL TIME CLOCK
_CLOCK = RTC()
try: 
    os.stat('timeflag') 
except:
    #<<CURRENT DATETIME: YYYY,MM,DD,0,HH,MM,SS,0
    _CLOCK.datetime((2023,12,26,0,9,55,0,0)) 
    open('timeflag','w').close()

print("Now is",time.localtime())

#SLEEP
def go_to_sleep(duration):
     minutes = duration//60
     seconds = (duration%60)
     
     #year,month,day,hour,min,sec,weekday,year_day
     dty,dtm,dtd,dth,dtmi,dtse,dtw,dtyd=time.localtime()
     print("now",dty,dtm,dtd,dth,dtmi,dtse,dtw,dtyd)
     
     #increment: 
     dtmi+=minutes
     dtse+=seconds

     #calculating next time
     futtime=time.mktime((dty,dtm,dtd,dth,dtmi,dtse,dtw,dtyd))
     
     interval = (futtime - time.time())
     interval_in_ms *= 1000
     
     print("fut", time.localtime(futtime))
     
     print("interval", interval_in_ms)
     if interval_in_ms > 0:
        if interval_in_ms > 900000: #no longer than 15 minutes
            deepsleep(900000)
        else:
            deepsleep(interval_in_ms)
     else:
        print("Cant sleep negative time")

     
#MAIN SENSOR CYCLE
def read_sensors(audio_length, data_interval, filepath):
  global FCount
  try:
    samples_loop = audio_length//data_interval
    header=False
    try:os.stat(filepath)
    except:header=True
    pen = open(filepath,"a+")
    if header: pen.write('timestamp,temperatura(C),umidade(%),pressao(Pa),gas(ohms),luminisidade(%);')
    lumin, temp, hum, pres, gas = 0,0,0,0,0
    for i in range(samples_loop):
        print("Collecting sampling",i)
        lumin = round(lumin+(adc.read_u16() / _MAXL * 100)/samples_loop,2)
        temp = round(temp+(bme.temperature/samples_loop), 2)
        hum = round(hum+(bme.humidity/samples_loop), 2)
        pres = round(pres+(bme.pressure/samples_loop), 2) #avg sea level: 1013,25 
        gas = round(gas+((bme.gas/1000)/samples_loop), 2) #values ranges in https://cdn-shop.adafruit.com/product-files/3660/BME680.pdf
        time.sleep(data_interval)
    print("Saving: {},{},{},{},{},{};".format(time.time(),temp,hum,pres,gas,lumin))
    pen.write("{},{},{},{},{},{};".format(time.time(),temp,hum,pres,gas,lumin))        
    pen.close()
  except OSError as e:
    print('Failed to read sensor.')


print("Start recording")
LED.set('orange')
_MIC.record(_AUDIO_FILE)
read_sensors(_AUDIO_LENGTH, _READINGS_INTERVAL, _LOG_FILE)
print("Stop recording")
_MIC.stop()
LED.set('black')
go_to_sleep(_SLEEP_TIME)
