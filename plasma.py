"""
Demoscene plasma effect for Adafruit NeoPixel BFF 5x5 LED Grid

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

class Plasma():
    def __init__(self):
        self.pixels = neopixel.NeoPixel(machine.Pin(29),5*5)
        self.pixels.fill((0,0,0))
        self.pixels.write()
        self.hearth_bitmap = [
            0,1,1,0,0,
            1,1,1,1,0,
            0,1,1,1,1,
            1,1,1,1,0,
            0,1,1,0,0,
        ]
        print("Plasma initialized.")

    def plasma(self,zoom):
        time=0
        pow=0.1
        print("Press Ctrl+C to quit.\n")
        while True:
            try:
                for p in range(25):
                    x=p%5-2
                    y=p/5-2
                    c=math.sin(math.sin(x*zoom+math.cos(time*0.3)*13) + math.cos(y*zoom+math.sin(time*.2)*17))
                    c=(128+int(c*128))*pow
                    if self.hearth_bitmap[24-p]==0:
                        c=c*0.025
                    self.pixels[p]=(
                        int(c+5+math.sin(time*0.21)*5),
                        int(c+5+math.cos(1+time*0.33)*5),
                        int(c+5+math.sin(1+time*0.47)*5))
                self.pixels.write()
                time+=0.05
            except KeyboardInterrupt:
                break
        
    def run(self, argument=0.33):
        self.plasma(argument)
        
if __name__ == '__main__':
    plasma = Plasma()
    plasma.run()
