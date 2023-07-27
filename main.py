"""
smolOS - boot script
-------------------------------------------------
Specialized Microcontroller-Oriented Lightweight Operating System

(c)2023/07 Krzysztof Krystian Jankowski
Homepage: https://smol.p1x.in/os/
"""
import machine
import utime
from smolos import smolOS

os=smolOS()

try:
    os.boot()
    print("Bye!")
except OSError:
    print("Oh, no!\n")
    utime.sleep(1)
    machine.soft_reset()