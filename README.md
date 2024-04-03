# EchoLogger Development Project

This repository contains the development project for EchoLogger, initiated and managed by the Institute of Computing (Instituto de Computação - IComp) at the Federal University of Amazonas (UFAM).

- **Project Leader and Coordinator:** Prof. PhD. Juan G. Colonna - [juancolonna@icomp.ufam.edu.br](mailto:juancolonna@icomp.ufam.edu.br)
- **Hardware Developer:** PhD. Márcio Alencar - [macalencar@gmail.com](mailto:macalencar@gmail.com)

## Contents

- **Hardware:** EasyEDA Project File and its variants as backups.
- **Software:** Micropython Firmware, basic libraries, and example codes.
- **Board Images:** Footprints, 2D/3D Images, and Logos.
- **Schematics:** Circuit schematics.
- **Documents:** General project documents, datasheets, and specifications.

## Project Overview

EchoLogger is a modularized low-cost development board project primarily aimed at monitoring environmental variables and recording sound. Its modular design facilitates the custom assembly of components to meet specific customer requirements. The device is tailored to streamline the non-industrialized production process by allowing the soldering of prefabricated components.

## Hardware Specifications

| TOP VIEW | BOTTOM VIEW|
|----------|------------|
|<img src="board images/hw_v3/BoardTop2D_v3.png" width="200"/>|<img src="board images/hw_v3/BoardBottom2D_v3.png" width="200"/>|

- **Dimensions:** 600mm (length) x 500mm (width) x 130mm (height)
- **Microcontroller:** ESP32-WROOM-32S (BLE 4.0 & WiFi 802.11 b/g)
- **Sensors:**
  - I2C 4x1 Sensor BME680 (Temperature, Humidity, Air Pressure & Air Quality)
  - I2S Mic for noise recording
  - SPI MicroSD Card Module
  - LDR Sensor
- **Connectivity:** USB-C Module
- **Power Regulation:** Voltage Regulator AP2112K-3.3V
- **User Interface:** Reset Button, Boot Firmware Loader Button, RGB Led (Common Cathode), On/Off Switch
- **Additional Features:** UART Exposed Pins, 4x 5mm Holes, Isolated sensors on the bottom face for safety exposure

## Power Specifications

### Supply
- **AP2112K-3.3V:** 2.8V~6.5V @ 800mA (Regulated to 3.3v @ 600mA)

### Operation mode
- **Reading Sensors:** 50mA
- **Micro SD Writing:** 70mA
- **Deepsleep:** 15mA
- **Waking Up:** 100mA
- **Bluetooth:** 170mA (RX) ~ 200mA (TX)
- **WiFi:** 170mA (RX) ~ 260mA (TX)

### Consumption Estimation
- **Routine:** 1 min recording, 5 min sleeping
- **Cycle:** Sleep -> Wake Up -> Record -> Save Data -> Back to Sleep
- **Power Consumption Estimation:** 30mAh (3.3V - 0.15Wh)

## Additional Information

[<img src="board images/logos/BannerATA.png" width="400"/>](ATA)

---
Feel free to reach out for any inquiries or collaborations!
