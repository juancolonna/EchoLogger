# Basic Libraries

This folder contains the basic libraries that help you to test the board funcionalities.

### RGBLib

Library that controlls the RGB led which is physically attached to the following ESP32 pins as follows:

- VCC: 3.3v
- RED: IO04
- GREEN: IO26
- BLUE: IO27

By using the `RGBLib` is is possible to instatiate an object that controlls the led as follow:

```
import RBGLib
LED = RBGLib.Controller(4,26,27)
LED.boot()

```

This library contains a set of pre-configured colors: `["black","red","green","blue","yellow","orange","pink","purple","cyan","white"]`. You may change the color by calling the method `LED.set('<COLOR>')`:

```
LED.set('blue')
LED.set('white')
LED.set('black')
LED.set('green')
```

You may also set manualy a led collor by define the RGB values using the method `LED.man(r,g,b)`. Each `r,g,b` values may assume any value from `0` to `1023`:

```
LED.man(100,200,300)
```


### BME680

This library controls the sensor [BME650](https://datasheet.lcsc.com/lcsc/1811141211_Bosch-Sensortec-BME680_C125972.pdf) by using a [SoftI2C](https://docs.micropython.org/en/latest/library/machine.I2C.html) classe which is connected to the board as the following:

- VCC: 3.3v
- GND: GND
- SDA: IO22
- SCL: IO21

You may create an object to controll the BME680 module by indicating a [SoftI2C](https://docs.micropython.org/en/latest/library/machine.I2C.html) object as following:

```
from machine import SoftI2C, Pin
import bme680

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
bme = BME680_I2C(i2c=i2c)

print("Temperature: {} ºC\n".format(bme.temperature))
print("Humidity: {} %".format(bme.humidity))
print("Air Pressure: {} HPa".format(bme.pressure))
print("Air Quality: {} IAQ".format(bme.gas))

```


### I2S Mic

This module controlls the [I2S](https://docs.micropython.org/en/latest/library/machine.I2S.html#machine.I2S) Microphone, it requires a [MicrSD Card](https://docs.micropython.org/en/latest/library/machine.SDCard.html) to store the recorded audio.

The SDCard module is connected to `ESP32`` as follows:

- VCC: 3.3v
- GND: GND
- CS: IO05
- MOSI: IO23
- CLK: IO18
- MISO: IO19

The I2SMic is connectes as follows:

- GND: GND
- VCC: 3.3v
- WS: IO25
- L/R: GND (it could be VCC)
- CK: IO32
- DA: IO33

Make sure that your sd card if formated as `FAT32` and inserted in the module's slot. After that, execute the following commands:

```
from machine import SDCard
import i2smic
import time

i2c = SDCard(slot=2)
os.mount(_SD, "/sd") 
MIC = i2smic.Controller()

MIC.record('/sd/output_file.wav')
time.sleep(10)
MIC.stop()

```

The `*.WAV` file are stored in the micro SD card.