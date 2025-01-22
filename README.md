# Screen mirroring python script for use with epaper display as a monitor via GPIO (SPI)

## ***This repo is only a proof of concept project, not even a first prototype.***

## Used display with driver and converter board from adafruit:
https://www.waveshare.com/6inch-HD-e-Paper-HAT.htm \
Documentation: \
https://www.waveshare.com/wiki/6inch_HD_e-Paper_HAT#Working_with_Raspberry_Pi_.28SPI.29

## Display driver based on this github project:
https://github.com/GregDMeyer/IT8951/tree/master
## Its README.md moved to README_driver.md
Currently not working on Raspberry Pi 5 because RPI.GPIO is not compatible with PI 5 so development was made on PI 4.

## Requirements:
It is recommended to run this project inside of a virtual environment. Needed packages are in requirements.txt.

## Enable SPI
In Raspberry PI OS SPI is off by default.
To enable it use:
```
sudo raspi-config
```
Then go to: Interface Options -> SPI -> Yes

## Switch to X11
For taking screenshots to work you need to switch from Wayland (default on Raspberry PI OS) to X11:
```
sudo raspi-config
```
Then go to: Advanced Options -> Wayland -> X11 -> Ok

## Helper scripts for screenshots:
While doing research and development on taking screenshots in python I made two helper programms using two different methods.
One is using X11 library, the other is using mss library.

## Screen mirroring systemd service
This proof of concept is intended to run on startup as a systemd service.
There is a service file:
```
screen_mirror.service
```
It needs to be copied to 
```
/etc/systemd/system/
```
Then you can enable and start the service:
```
sudo systemctl enable screen_mirror.service
```
```
sudo systemctl start screen_mirror.service
```
After any changes done to service file you need to reload configuration:
```
sudo systemctl daemon-reload
```
The restart the service:
```
sudo systemctl restart screen_mirror.service
```
