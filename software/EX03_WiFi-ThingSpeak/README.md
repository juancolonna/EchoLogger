# Wifi + Thingspeak

This folder contains an example how to send data from your device to the [Thingspeak](https://thingspeak.com/) over wifi.

### Lib mrequests

This code uses a library called [mrequests)[https://github.com/SpotlightKid/mrequests] that implements the main REST methods (`GET, POST, PUT, UPDATE & DELETE`). To use it, run:

```
ampy -b 115200 -p COM6 put ./EX03_WIfi-Thingspeak/mrequests.py mrequests.py
```

Befor upload the `main.py` we need to update the `_APIKEY` value. This key must be generated in the section `API Keys > Write API Key` from [Thingspeak](https://thingspeak.com) dashboard. Make sure your Channel Settings contains 5 Fields at this order `Temperature, Humidity, Air Pressure, Air Quality` and `Light Intensity`:

```
#Thingspeak
_APIKEY = "YOUR_API_KEY_HERE"
_URL='https://api.thingspeak.com/update?api_key={}&field1={}&field2={}&field3={}&field4={}&field5={}'
```

You might have to include your Wifi's name (`_SSID``) and its password (`_PWD``)

```
#Wifi Credentials
_SSID="YOUR_SSID_HERE"
_PWD ="WIFI_PASSWORD_HERE"
```

Save the file and upload it to the board

```
ampy -b 115200 -p COM6 put ./EX03_WIfi-Thingspeak/main.py main.py
```

After that, reboot your device and access your [Thingspeak](https://thingspeak.com). 

Note: The API ignores demands an interval of 30s  between the last and a new request.