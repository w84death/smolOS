"""
Pixel - tools for playing with one NeoPixel

(c)2023/07 Krzysztof Krystian Jankowski
Homepage: https://smol.p1x.in/os/
"""

import machine
import neopixel
import _thread
import utime

class Pixel:
    """
    A class to handle a single NeoPixel LED.
    """
    HEARTBEAT_PATTERN = [0, 10, 20, 50, 100, 255, 200, 100, 50, 30, 20, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    BREATHE_DELAY = 0.05
    HEARTBEAT_DELAY = 0.05

    def __init__(self, pin=12):
        """
        Initialize the NeoPixel object.
        """
        self.thread_running = False
        self.power = machine.Pin(11, machine.Pin.OUT)
        self.power.value(1)
        self.pixel = neopixel.NeoPixel(machine.Pin(pin), 1)
        print("NeoPixel: Initialized. Use pixel.start(), pixel.stop(), pixel.color('r,g,b').")

    def color(self, color=(0, 0, 0)):
        """
        Set the color of the NeoPixel.
        """
        self.pixel.fill(color)
        self.pixel.write()

    def stop(self):
        """
        Stop the animation.
        """
        self.thread_running = False
        print("NeoPixel: Hearthbeat stopped. Use pixel.start()")

    def start_threaded(self):
        """
        Start the animation in a new thread.
        """
        if not self.thread_running:
            self.thread_running = True
            _thread.start_new_thread(self.breath, ())
            print("NeoPixel: Hearthbeat started in background. Use pixel.stop()")

    def start_unthreaded(self):
        """
        Start the animation in the current thread.
        """
        if not self.thread_running:
            self.thread_running = True
            self.heartbeat()

    def heartbeat(self):
        """
        Animate the NeoPixel with a "heartbeat" pattern.
        """
        while self.thread_running:
            for brightness in self.HEARTBEAT_PATTERN:
                red = int((255 * brightness) / 255)
                green = int((105 * brightness) / 255)
                blue = int((180 * brightness) / 255)

                self.pixel.fill((red, red, red))
                self.pixel.write()
                utime.sleep(self.HEARTBEAT_DELAY)

    def breath(self):
        """
        Animate the NeoPixel with a "breath" pattern.
        """
        while self.thread_running:
            for brightness in range(255):
                white = int((255 * brightness) / 255)
                self.pixel.fill((white, white, white))
                self.pixel.write()
                utime.sleep(self.BREATHE_DELAY)
            utime.sleep(1)
            for brightness in range(255):
                white = 255 - int((255 * brightness) / 255)
                self.pixel.fill((white, white, white))
                self.pixel.write()
                utime.sleep(self.BREATHE_DELAY)


# pixel = Pixel(pin=12)  # replace 'pin' with the number of the pin that the NeoPixel is connected to
# pixel.color((255, 0, 0))  # set the color to red
# pixel.color((0, 255, 0))  # set the color to green
# pixel.color((0, 0, 255))  # set the color to blue
# pixel.start_threaded()  # start the 'breath' animation in a new thread
# pixel.start_unthreaded()  # start the 'heartbeat' animation in the current thread
# pixel.stop()
