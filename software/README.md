# Software Examples

This is folder contain the basic firmware and some python codes available for testing the board.

For that you may install the [esptool.py](https://github.com/espressif/esptool) for burning the firmware in the ESP, use the [mpy-cross](https://gitlab.com/alelec/mpy_cross) to 'compile' the `.py` codes and save some space, and then, send the `*.mpy` compiled files to the board using the [adafruit-ampy](https://github.com/scientifichackers/ampy) tool and a serial module.

Note: This tutorial used `Python 3.10.6`

### Install the requirements tools
```
pip install esptool
pip install adafruit-ampy
pip install mpy-cross
```

### Flashing the Micropython Firmware

1. Connect the power supply (5v) to the USB-C connector.
2. Connect the [Serial Module](https://www.smartkits.com.br/conversor-ftdi-ft232rl-com-chave-3-3v5v-vermelho?parceiro=9390&gad_source=1&gclid=Cj0KCQiAkKqsBhC3ARIsAEEjuJiISQHI6NMQX0_4cwJt9-WwlSEjd3k5F9d2lmZSCOJGGaLRyTsUmu4aAsqQEALw_wcB) (at 3.3v only) to the UART pins on the board (No need to connect VCC).
3. Identify the serial port of your serial module (Example using Windows - COM6).
4. Holding the `Boot/BTN` down, press & relase the `Reset` button.
5. Run the following command.

```
python -m esptool --chip esp32 --port COM6 erase_flash
```

After that, reset your device, execute the steps `4` and `5` again and run:

```
python -m esptool --chip esp32 --port COM6 --baud 460800 write_flash -z 0x1000 ./Micropython/ESP32_GENERIC-20231005-v1.21.0.bin
```

Reset the board again and it's done! Now your device has the Micropython firmware installed. 

We recommend to use the latest [Micropython for ESP32-WROOM](https://micropython.org/download/ESP32_GENERIC/) Version.

### Uploading the Demo Codes

This section describes how to send the basic library, available in `EX00_BasicLibs`, and use them in a demo application, available in `EX01_Bluetooth`. This demo tests all reseouces available in the board (mic, sensor, led, sdcard and bluetooth).

By using the [adafruit-ampy](https://github.com/scientifichackers/ampy) tool, you must save the basic library into the controller, for that, run the following commands:

```
ampy -b 115200 -p COM6 put ./EX00_BasicLibs/ble_advertising.py ble_advertising.py 
ampy -b 115200 -p COM6 put ./EX00_BasicLibs/bme680.py bme680.py 
ampy -b 115200 -p COM6 put ./EX00_BasicLibs/i2smic.py i2smic.py 
ampy -b 115200 -p COM6 put ./EX00_BasicLibs/RGBLib.py RGBLib.py 
```

Finally, save the main code `main.py` to run the device as a BLE Advertiser. For that you may install the `EchoLogger.apk` (Recommended) app in the `EX00_Extras` or use the `NRFConnect` from [PlayStore](https://play.google.com/store/apps/details?id=no.nordicsemi.android.mcp&pcampaignid=web_share) or [AppleStore](https://apps.apple.com/br/app/nrf-connect-for-mobile/id1054362403?platform=iphone).

```
ampy -b 115200 -p COM6 put ./EX01_Bluetooth/boot.py main.py 
```

Now, reset the device, run the app in yout smartphone, and connect to device called `EchoLogger`(NRFConnect) or click `Find and Connect` (EchoLogger.apk`)

Done!

### Connecting to the board using UART

Open you terminal monitor (suggested: [VSCode Serial Monitor by Microsoft](https://github.com/microsoft/vscode-serial-monitor_)) and connect to the board using the following configuration:

- Monitor Mode: Serial
- View Mode: Text
- Port: COM6 (*just following the previous example)
- Baud Rata: 115200
- Line ending: CRLF
- Data Bits: 8
- Stop bits: 1
- Parity: None
- DTR:  Checked
- RST: Checked

If everything went well, your device is ready to run your python commands.

This communication allows to interact with the Micropython terminal and run commands on demand, for example: 

```
print("Hello World")
```

Visit the [Micropython Documentation](https://docs.micropython.org/en/latest/) page for further informations on how to interacts with Micropython.
