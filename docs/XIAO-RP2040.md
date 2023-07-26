# Install smolOS on XIAO RP2040

DRAFT

## Instal Frest MicorPython
Download latest firmware.
* Long press `boot` button on the XIAO
* Plug into the USB while still pressing
* Push after 1 sec
* New devce shoudl popup
* Mount the drive
* Copy firmware to it
* XIAO will restart itself

## Pushing smolOS
**Rename downloaded sources to main.py**
### Prepare Envronment
Do this once
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install ampy
```

Next time
```
$ source venv/bin/activate
$ ampy --port /dev/ttyUSB0 put main.py
$ ampy --port /dev/ttyUSB0 put hello.txt
```
- main.py is the smolOS, this file name will run at boot
- hello.txt is just a test file so you have something to play with
- put your own files the same way
- **do not** ovevrite the system boot.py file!
