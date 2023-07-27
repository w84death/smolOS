"""
Yellow Rubber Duck for programmers

(c)2023/07 Krzysztof Krystian Jankowski
Homepage: https://smol.p1x.in/os/
"""

import utime
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
        self.name = "Yellow Duck"
        self.pixels = neopixel.NeoPixel(machine.Pin(29),5*5)
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

    def hello(self):
        """
        Play a duck animation in a new thread.
        """
        self.msg("Aproching..")
        anim_intro = self.animations["buddy"][:4]
        for frame in anim_intro:
            self.draw(frame)
            utime.sleep(1)

        anim = self.animations["buddy"][4:]
        self.msg("Swims to you!\nExplain your problem now. Press Ctrl+C to quit.\n")
        while True:
            try:
                frame = random.choice(anim)
                self.draw(frame)
                utime.sleep(random.uniform(0.25, 2.0))
            except KeyboardInterrupt:
                self.bye()
                break

    def bye(self):
        """
        Stop the duck animation.
        """
        anim_outro = self.animations["buddy"][:4][::-1]
        self.msg("Duck swims away...")
        for frame in anim_outro:
            self.draw(frame)
            utime.sleep(1)
            self.pixels.fill((0,0,0))
            self.pixels.write()


    def msg(self, message):
        """
        Print a message from the program.
        """
        print(f"{self.name} : {message}")

if __name__ == '__main__':
    duck = Duck()
    duck.hello()