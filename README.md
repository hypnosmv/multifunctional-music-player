# Multifunctional Music Player

Raspberry Pi 4 Model B that plays music tracks from RFID cards.

## Showcase

https://github.com/user-attachments/assets/bab8813d-467f-437f-9b2b-9f828e479c90

## Overview

Placing a keycard on the RFID module starts playing a music track (unique to that card). Playback is carried out in two modes, either through a Raspberry Pi with a connected Bluetooth speaker (default) or via a smartphone. The current mode is indicated by one of the two LEDs, and switching between modes is executed by pressing the blue switch once. If the mode is switched during playback, the playback progress remains consistent.

The volume of playback through the Raspberry Pi is controlled by a potentiometer and indicated by an LED bar. Playback can be stopped immediately by pressing the red switch. During playback, the first LCD screen displays the track title, artist, and playback progress, while the second screen shows the album cover.

## Component list

- Raspberry Pi 4 Model B
- RFID module RC522 + keycards
- LCD1602 I2C
- LCD 1.54'' 240x240 SPI with ST7789 driver
- ADC module ADS7830
- Rotary potentiometer 10 kOhm
- LED bar graph
- 2x Tactile switch
- 2x LED
- 2x Shift register 74HC595
- 12x Resistor 220 Ohm
- 4x Resistor 10 kOhm

## Diagrams

![connections](https://github.com/user-attachments/assets/e2e76a5e-da26-4014-99f3-c0010ce69d04)

Control module:\
![control_module](https://github.com/user-attachments/assets/206abfa7-339b-4de2-b2a0-a4551b51c2a8)

LED module:\
![led_module](https://github.com/user-attachments/assets/7738d527-8ae6-4cd0-958f-a16bbba72d35)

## Code architecture

The chosen code architecture primarily aims to clearly separate different areas of responsibility and to support code modularity.

The system is based on Python threads. Most threads handle a single component or a category of components, while all threads have a specific responsibility (for example, controlling LEDs) and use at least one shared variable (such as a variable storing the number of the currently played track).

## Requirements

- I2C configured + address mapping
- SPI configured
- adb for linux
- amixer for linux
- python3 + packages
- USB debugging + security options disabled
- VLC for Android

## Credits and licences

Required credits are listed in the `credits.txt` file.\
All files located in the `src/lib` directory are licensed (see details in the `src/lib/licenses.txt` file).\
Files that are located directly in the `src` directory are covered by the license provided in the `LICENSE` file.
