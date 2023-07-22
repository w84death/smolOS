# Plasma effect for Adafruit NeoPixel BFF 5x5 LED Grid
import machine
import utime
import _thread
import time
import neopixel
import math
import random

class neo_plasma():
    def __init__(self):
        self.thread_running = False

        self.pixels = np = neopixel.NeoPixel(machine.Pin(29),5*5)
        self.pixels.fill((0,0,0))
        self.pixels.write()
        self.brightness = 0.2

        self.hearth_bitmap = [
            0,1,1,0,0,
            1,1,1,1,0,
            0,1,1,1,1,
            1,1,1,1,0,
            0,1,1,0,0,
        ]

    def plasma(self):
        time=0
        zoom=0.33
        pow=0.1
        while self.thread_running:
            for p in range(25):
                x=p%5-2
                y=p/5-2
                c=math.sin(math.sin(x*zoom+math.cos(time*0.3)*13) + math.cos(y*zoom+math.sin(time*.2)*17))
                c=(128+int(c*128))*pow
                if self.hearth_bitmap[24-p]==0:
                    c=c*0.025
                self.pixels[p]=(
                    int(c+5+math.sin(time*0.21)*5),
                    int(c+5+math.cos                                                                                                (1+time*0.33)*5),
                    int(c+5+math.sin(1+time*0.47)*5))
            self.pixels.write()
            time+=0.05

    def demo(self):
        self.start(self.plasma)

    def stop(self):
        self.thread_running = False
        print("NeoPixel: Thread stopped. Use plasma.demo()")

    def start(self,fn):
        if not self.thread_running:
            self.thread_running = True
            _thread.start_new_thread(fn,())
            print("NeoPixel: Demo thread started in background. Use plasma.stop()")
        else:
            print("NeoPixel: Thread already used. Use plasma.stop()")

#plasma = neo_plasma()