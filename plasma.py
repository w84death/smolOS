"""
Plasma effect for Adafruit NeoPixel BFF 5x5 LED Grid

(c)2023/07 Krzysztof Krystian Jankowski
Homepage: https://smol.p1x.in/os/
"""

import machine
import utime
import _thread
import time
import neopixel
import math
import random

# Define constants
LED_PIN = 29
LED_COUNT = 5*5
PLASMA_SPEED = 0.05
ZOOM = 0.33
BRIGHTNESS_POW = 0.1

# Define neo_plasma class
class NeoPlasma:
    """
    A class to handle the NeoPlasma functionalities.
    """
    def __init__(self):
        """
        Initialize the NeoPlasma object.
        """
        self.thread_running = False
        self.pixels = np = neopixel.NeoPixel(machine.Pin(LED_PIN), LED_COUNT)
        self.pixels.fill((0,0,0))
        self.pixels.write()
        self.brightness = BRIGHTNESS_POW
        self.hearth_bitmap = [
            0,1,1,0,0,
            1,1,1,1,0,
            0,1,1,1,1,
            1,1,1,1,0,
            0,1,1,0,0,
        ]

    def calculate_color(self, time, p):
        """
        Calculate color for the pixel.
        """
        x = p%5-2
        y = p/5-2
        c = math.sin(math.sin(x*ZOOM+math.cos(time*0.3)*13) + math.cos(y*ZOOM+math.sin(time*.2)*17))
        c = (128+int(c*128))*BRIGHTNESS_POW
        if self.hearth_bitmap[24-p] == 0:
            c = c*0.025
        return (
            int(c+5+math.sin(time*0.21)*5),
            int(c+5+math.cos(1+time*0.33)*5),
            int(c+5+math.sin(1+time*0.47)*5)
        )

    def plasma(self):
        """
        Create a plasma effect.
        """
        time = 0
        while self.thread_running:
            for p in range(LED_COUNT):
                self.pixels[p] = self.calculate_color(time, p)
            self.pixels.write()
            time += PLASMA_SPEED

    def demo(self):
        """
        Demo the plasma effect.
        """
        self.start(self.plasma)

    def stop(self):
        """
        Stop the plasma effect.
        """
        self.thread_running = False
        print("NeoPixel: Thread stopped. Use plasma.demo()")

    def start(self, fn):
        """
        Start the plasma effect.
        """
        if not self.thread_running:
            self.thread_running = True
            _thread.start_new_thread(fn, ())
            print("NeoPixel: Demo thread started in background. Use plasma.stop()")
        else:
            print("NeoPixel: Thread already used. Use plasma.stop()")

# plasma = NeoPlasma()
# plasma.demo()
