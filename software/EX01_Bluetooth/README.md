# BLE Demo

This folder contains the main code for a basic application using [Bluetooth Low Energy](https://docs.micropython.org/en/latest/library/bluetooth.html)

### BLE Service

This demos advertised the services as `Environmental Sensing Service` (`0x181A`) as defined [BLESpecifications](https://github.com/macalencar/PC20230001/tree/main/05_Docs/BLESpecifications)

This devices propagates the following characteristics :

- **Serial RX:** 6E400002-B5A3-F393-E0A9-E50E24DCCA9E   (Receive Data)
- **Serial TX:** 6E400002-B5A3-F393-E0A9-E50E24DCCA9E   (Transmit Data)
- **Air Pressure:** 0x2A6D
- **Temperature:** 0x2A6E
- **Humidity:** 0x2A6F
- **Air Quality:** 0x2AF9
- **Illuminance:** 0x2AFB
- **Device Time:** 0x2B90
- **Storege Free Space**: 0x2B04

This demo propagates the device name as `EchoLogger` and all values are published as a `Float 16`.

For further information go to [Bluetooth.org](https://www.bluetooth.com/bluetooth-resources/intro-to-bluetooth-low-energy/) or check the [Micropython BLE Documentation](https://docs.micropython.org/en/latest/library/bluetooth.html)
