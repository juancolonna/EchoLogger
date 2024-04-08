import os
import time
from machine import Pin, SoftI2C, ADC, Timer, RTC, Timer, SDCard
import machine
import bme680
import RGBLib
import i2smic
#TIMERS

UPDTimer=Timer(2)
lumin, temp, hum, pres, gas = 0,0,0,0,0

# LDR SENSOR (ANALOGIC INTERFACE)
adc = ADC(Pin(34), atten=ADC.ATTN_6DB) #10kOhm - 3.3v
_MAXL = 65535

# BMP680 SENSOR (I2C INTERFACE)
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
bme = bme680.BME680_I2C(i2c=i2c)

#I2s Microphone
_MIC = i2smic.Controller()
_SENSORS_FILE="/sd/data.txt"
_AUDIO_FILE="/sd/record-{}".format(time.time())
_AUDIO_LENGTH=300 #s
_READINGS_INTERVAL=30 #s
_SAMPLES_LOOPS=_AUDIO_LENGTH//_READINGS_INTERVAL
# LED CONTROLLER
LED = RGBLib.Controller(4,26,27)

_CLOCK=RTC()
try:
    _=os.stat("/timeflag.tmp") 
except:
    _CLOCK.datetime((2024,3,14,0,22,8,0,0)) 
    with open("/timeflag.tmp","w") as fp:
        fp.write("ok")




# SDCARD MODULE (SPI INTERFACE)
sd = SDCard(slot=2)  # sck=18, mosi=23, miso=19, cs=5
os.mount(sd, "/sd")

#MAIN SENSOR CYCLE
def read_sensors(t):
    global lumin, temp, hum, pres, gas, _SAMPLES_LOOPS
    print("Collecting Sample")
    lumin = round(lumin+(adc.read_u16() / _MAXL * 100)/_SAMPLES_LOOPS,2)
    temp = round(temp+(bme.temperature/_SAMPLES_LOOPS), 2)
    hum = round(hum+(bme.humidity/_SAMPLES_LOOPS), 2)
    pres = round(pres+(bme.pressure/_SAMPLES_LOOPS), 2) #avg sea level: 1013,25 
    gas = round(gas+((bme.gas/1000)/_SAMPLES_LOOPS), 2) #values ranges in https://cdn-shop.adafruit.com/product-files/3660/BME680.pdf
    print("Sampling: {},{},{},{},{},{};".format(time.time(),temp,hum,pres,gas,lumin))
    
print("Now is",time.localtime())
LED.set('orange')

UPDTimer.init(period=_READINGS_INTERVAL*1000, mode=Timer.PERIODIC, callback=read_sensors)

_MIC.record(_AUDIO_FILE)
time.sleep(_AUDIO_LENGTH)
UPDTimer.deinit()
_MIC.stop() 

header=False
try:os.stat(_SENSORS_FILE)
except:header=True
pen = open(_SENSORS_FILE,"a+")
if header: pen.write('timestamp,temperatura(C),umidade(%),pressao(Pa),gas(ohms),luminisidade(%);audio;')
print("Saving: {},{},{},{},{},{};".format(time.time(),temp,hum,pres,gas,lumin,_AUDIO_FILE))
pen.write("{},{},{},{},{},{};".format(time.time(),temp,hum,pres,gas,lumin,_AUDIO_FILE))        
pen.close()
    
print("Done")
machine.deepsleep(_AUDIO_LENGTH*1000)


