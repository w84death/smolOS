# Yellow Rubber Duck for programmers
import utime
import _thread
import time
import neopixel
import math
import random

class Duck():
    def __init__(self):
        self.thread_running = False

        self.pixels = np = neopixel.NeoPixel(machine.Pin(29),5*5)
        self.pixels.fill((0,0,0))
        self.pixels.write()
        self.brightness = 0.2
        self.palette = [
            (0,0,0),
            (50,50,25),
            (0,0,0),
            (0,0,0),
            (0,0,0),
            (10,10,10),
            (128,50,20),
            (0,12,10)]

        self.buddy0_bitmap = [
            7,7,7,7,7,
            7,7,7,7,7,
            7,7,7,7,7,
            7,7,7,7,7,
            7,7,7,7,7,
        ]
        self.buddy1_bitmap = [
            7,7,7,7,7,
            7,7,7,7,7,
            7,7,7,1,7,
            7,7,7,5,7,
            7,7,7,7,7,
        ]
        self.buddy2_bitmap = [
            7,7,7,7,7,
            7,7,7,7,7,
            7,7,0,1,7,
            7,7,5,5,7,
            7,7,7,7,7,
        ]
        self.buddy3_bitmap = [
            7,7,7,7,7,
            7,1,0,1,7,
            7,1,1,6,7,
            7,1,0,1,7,
            7,7,7,7,7,
        ]
        self.buddy4_bitmap = [
            1,0,1,1,5,
            1,1,6,1,1,
            1,0,1,1,1,
            7,7,7,1,5,
            7,7,7,5,7,
        ]
        self.buddy5_bitmap = [
            1,5,1,1,5,
            1,1,6,1,1,
            1,5,1,1,1,
            7,7,7,1,5,
            7,7,7,5,7,
        ]
        self.buddy6_bitmap = [
            7,1,6,1,5,
            1,0,1,1,1,
            1,1,1,1,1,
            7,7,7,1,5,
            7,7,7,5,7,
        ]
        self.buddy7_bitmap = [
            1,1,1,1,5,
            1,0,1,1,1,
            7,1,6,1,1,
            7,7,7,1,5,
            7,7,7,5,7,
        ]
        self.buddy8_bitmap = [
            7,1,0,1,5,
            7,1,1,6,1,
            7,1,0,1,1,
            7,7,5,1,5,
            7,7,1,7,7,
        ]


    def draw(self,bitmap):
        for i in range(25):
            self.pixels[24-i]=self.palette[bitmap[i]]
        self.pixels.write()

    def duck_thread(self):
        anim_intro = [
            self.buddy0_bitmap,
            self.buddy0_bitmap,
            self.buddy1_bitmap,
            self.buddy0_bitmap,
            self.buddy1_bitmap,
            self.buddy2_bitmap,
            self.buddy3_bitmap,
            self.buddy4_bitmap,
        ]
        for frame in anim_intro:
            self.draw(frame)
            utime.sleep(1)

        anim = [
            self.buddy4_bitmap,
            self.buddy5_bitmap,
            self.buddy6_bitmap,
            self.buddy7_bitmap,
            self.buddy8_bitmap,
        ]
        while self.thread_running:
            frame = random.choice(anim)
            self.draw(frame)
            utime.sleep(random.uniform(0.25, 2.0))

    def bye(self):
        anim_outro = [
            self.buddy5_bitmap,
            self.buddy3_bitmap,
            self.buddy2_bitmap,
            self.buddy1_bitmap,
            self.buddy0_bitmap,
        ]
        self.thread_running = False
        print("Duck swimps away...")
        for frame in anim_outro:
            self.draw(frame)
            utime.sleep(1)
        print("Use duck.hello()")
        self.pixels.fill((0,0,0))
        self.pixels.write()

    def hello(self):
        if not self.thread_running:
            self.thread_running = True
            _thread.start_new_thread(self.duck_thread,())
            print("Duck swims to you!.\nExplain your problem now.\nUse duck.bye() to stop.")
        else:
            print("Duck: Thread already in use. Kill other backround programs.")

duck  = Duck()
duck.hello()
