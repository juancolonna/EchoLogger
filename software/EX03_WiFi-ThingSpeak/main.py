import network
import os
import time
from machine import Pin, Timer, SoftI2C, ADC, Timer, RTC, Timer
import bme680
import RGBLib
import mrequests
import ntptime

#Thingspeak
_APIKEY = "NZEKR612C60Y0PL1" #<<--CHANGE THIS
_URL='https://api.thingspeak.com/update?api_key={}&field1={}&field2={}&field3={}&field4={}&field5={}'

#Wifi Credentials
_SSID="WLANCutia" #<<--CHANGE THIS
_PWD ="!1a2b_3c4d!E" #<<--CHANGE THIS


#UPDATE TIMER
UpdatePeriod=5000
UPDTimer=Timer(2)

#RGB LED
LED = RGBLib.Controller(4,26,27)

# LDR SENSOR (ANALOGIC INTERFACE)
adc = ADC(Pin(34), atten=ADC.ATTN_6DB) #10kOhm - 3.3v

_MAXL = 65535

# BMP680 SENSOR (I2C INTERFACE)
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
bme = bme680.BME680_I2C(i2c=i2c)

_NET = None

def readSensor():
     global bme, adc, _MAXL
     pkg = {}
     pkg["temp"]=round(bme.temperature, 2) # ºC
     pkg["humi"]=round(bme.humidity, 2) # %
     pkg["pres"]=round(bme.pressure, 2) #avg sea level: 1013,25 
     pkg["lumi"]=int(round((adc.read_u16() / _MAXL * 100),2))
     pkg["aqua"]=round(bme.gas/1000, 2) #values ranges in https://cdn-shop.adafruit.com/product-files/3660/BME680.pdf
     return pkg

def send_package(FilledURL):
    try: 
        print(FilledURL)
        response = mrequests.request('GET',FilledURL)
        print("send_package: got", response.status_code)#, response.content, "on sending", PKG)
        print("send_package: content", response.content)
        if response.status_code == 200: return True
        return False
    except Exception as e: 
        raise Exception("(send_pkg): error on {}".format(str(e)))


def load_wifi(ssid, pwd):
     global _NET
     _NET = network.WLAN(network.STA_IF)
     _NET.active(True)
     time.sleep(1)
     _NET.config(dhcp_hostname="EchoLogger")
     time.sleep(1)
     _NET.connect(ssid,pwd)
     for _ in range(10):
          LED.set('cyan')
          if _NET.isconnected(): 
                LED.set('green')
                return True
          LED.set('red')
          time.sleep(3)
     return False
 

def uploadValues(t):
     global _URL, _APIKEY
     #THINGSPEAK - Public View @ https://thingspeak.com/channels/2390384#
     #Fields: 1-Temperature, 2-Humidity, 3-AirPressure, 4-AirQuality, 5-LightIntensity
     LED.set('orange')
     
     data = readSensor()
     #Fields: 1-Temperature, 2-Humidity, 3-AirPressure, 4-AirQuality, 5-LightIntensity     
     if send_package(_URL.format(_APIKEY, data['temp'],data["humi"],data["pres"],data["aqua"],data["lumi"])):
          LED.set('green')
     else:
          LED.set('red')
     time.sleep(3)
     LED.set('cyan')

#BUTTON HANDLER
def btn_callback(t):
     if BTN.value()==0:
          print("Emergency break!")   
          UPDTimer.deinit()
     time.sleep(2)
     print("Terminal Unlocked")
     
BTN = Pin(0, Pin.IN)       
BTN.irq(trigger=Pin.IRQ_FALLING, handler=btn_callback)

     
#--------------------------------- BOOT ----------------------------------------#

LED.boot()

if load_wifi(_SSID,_PWD):
     ntptime.settime()
     print("current time {}".format(str(time.localtime())))
     UPDTimer.init(period=30000, mode=Timer.PERIODIC, callback=uploadValues)


