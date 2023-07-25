"""
Yellow Rubber Duck for programmers
"""
import utime
import _thread
import time
import neopixel
import math
import random

class Duck:
    """
    A class to handle the Duck functionalities.
    """
    def __init__(self):
        """
        Initialize the Duck object.
        """
        self.thread_running = False
        self.pixels = np = neopixel.NeoPixel(machine.Pin(29),5*5)
        self.pixels.fill((0,0,0))
        self.pixels.write()
        self.brightness = 0.2
        self.palette = [
            (0,0,0),
            (50,50,25),
            (10,10,10),
            (128,50,20),
            (0,12,10)
        ]

        # Define animation frames
        self.animations = {
            "buddy": [
                [
                    4,4,4,4,4,
                    4,4,4,4,4,
                    4,4,4,4,4,
                    4,4,4,4,4,
                    4,4,4,4,4,
                ],
                [
                    4,4,4,4,4,
                    4,4,4,4,4,
                    4,4,4,1,4,
                    4,4,4,2,4,
                    4,4,4,4,4,
                ],
                [
                    4,4,4,4,4,
                    4,4,4,4,4,
                    4,4,0,1,4,
                    4,4,2,2,4,
                    4,4,4,4,4,
                ],
                [
                    4,4,4,4,4,
                    4,1,0,1,4,
                    4,1,1,3,4,
                    4,1,0,1,4,
                    4,4,4,4,4,
                ],
                [
                    1,0,1,1,2,
                    1,1,3,1,1,
                    1,0,1,1,1,
                    4,4,4,1,2,
                    4,4,4,2,4,
                ],
                [
                    1,2,1,1,2,
                    1,1,3,1,1,
                    1,2,1,1,1,
                    4,4,4,1,2,
                    4,4,4,2,4,
                ],
                [
                    4,1,3,1,2,
                    1,0,1,1,1,
                    1,1,1,1,1,
                    4,4,4,1,2,
                    4,4,4,2,4,
                ],
                [
                    1,1,1,1,2,
                    1,0,1,1,1,
                    4,1,3,1,1,
                    4,4,4,1,2,
                    4,4,4,2,4,
                ],
                [
                    4,1,0,1,2,
                    4,1,1,3,1,
                    4,1,0,1,1,
                    4,4,2,1,2,
                    4,4,1,4,4,
                ],
            ]
        }

    def draw(self,bitmap):
        """
        Draw a specific frame.
        """
        for i in range(25):
            self.pixels[24-i]=self.palette[bitmap[i]]
        self.pixels.write()

    def duck_thread(self):
        """
        Play a duck animation in a new thread.
        """
        anim_intro = self.animations["buddy"][:4]
        for frame in anim_intro:
            self.draw(frame)
            utime.sleep(1)

        anim = self.animations["buddy"][4:]
        while self.thread_running:
            frame = random.choice(anim)
            self.draw(frame)
            utime.sleep(random.uniform(0.25, 2.0))

    def start_unthreaded(self):
        """
        Start the duck animation in the current thread.
        """
        if not self.thread_running:
            self.thread_running = True
            self.duck_thread()
            print("Duck swims to you!\nExplain your problem now.")

    def start_threaded(self):
        """
        Start the duck animation in a new thread.
        """
        if not self.thread_running:
            self.thread_running = True
            _thread.start_new_thread(self.duck_thread,())
            print("Duck swims to you!\nExplain your problem now.")

    def stop(self):
        """
        Stop the duck animation.
        """
        anim_outro = self.animations["buddy"][4:][::-1]
        self.thread_running = False
        print("Duck swims away...")
        for frame in anim_outro:
            self.draw(frame)
            utime.sleep(1)
        print("Use start_unthreaded() or start_threaded() to start.")
        self.pixels.fill((0,0,0))
        self.pixels.write()

# To use this refactored code, you would do something like the following:
# duck = Duck()
# duck.start_unthreaded()  # to start the duck animation in the current thread
# or
# duck.start_threaded()  # to start the duck animation in a new thread
# duck.stop()  # to stop the duck animation

