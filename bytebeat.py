"""
Bytebeat implementation for smolOS/NeoPixel(s)

(c)2023/08 Krzysztof Krystian Jankowski
Homepage: https://smol.p1x.in/os/
"""
import machine
from machine import Pin, PWM
import utime
import math
import neopixel


BUZZER_PIN = 3
BUZZER_DUTY = 32768
PI = 3.1415926535
PI2 = PI*2
NEOPIXEL_PIN = 12
NEOPIXELS_PIN = 29

sin = math.sin

class ByteBeat:
    def __init__(self):
        self.t = 512
        self.pixel = neopixel.NeoPixel(machine.Pin(NEOPIXEL_PIN), 1)
        self.power = machine.Pin(NEOPIXEL_PIN-1, machine.Pin.OUT)
        self.power.value(1)
        self.pixels = neopixel.NeoPixel(machine.Pin(NEOPIXELS_PIN), 25)
        self.pixels.fill((0,0,0))
        self.pixels.write()
        self.buzzer = PWM(Pin(BUZZER_PIN, Pin.OUT))
        self.buzzer.duty_u16(BUZZER_DUTY)

    # bytebeat formula
    def bytebeat(self, t):
        '''
        #1 Crazy Scientist Tune
        return [
            int((127+128*sin(0.285714*(t&t>>8)+7.71429)*PI2)*.01),
            int((127+128*sin((1.11905*(t>>10)+7.71429+(2*sin(t>>8)))*PI2))),
            int(31+32*sin((4.8*(t>>11)*PI)))>>4
        ]
        '''
        #2 Acid techno
        return [
            int(t&(1024+t%1024)>>3)>>2, # acid bass
            int(((10000/(1+t%1024)))), # bum bum
            int((t>>2)^((t>>4)%883)) # main mellody
        ]

    def play(self):
        print("ByteBeat Player")
        print("Press Ctrl+C to quit.\n")
        print("\nPlaying: t&(1024+t%1024)>>3)>>2 | ((10000/(1+t%1024))) | (t>>2)^((t>>4)%883)\n")
        while True:
            try:
                bb=self.bytebeat(self.t)
                bites = bb[0] | bb[1] | bb[2]
                if(bites%512>10):
                    self.buzzer.freq(bites%512)
                self.t += 1
                color = (int(bb[0]%255),int(bb[1]%255),int(bb[2]%255))
                self.pixels.fill(color)
                self.pixel.fill(color)
                self.pixels.write()
                self.pixel.write()

            except KeyboardInterrupt:
                self.buzzer.duty_u16(0)
                self.pixels.fill((0,0,0))
                self.pixel.fill((0,0,0))
                self.pixels.write()
                self.pixel.write()
                break


if __name__ == "__main__":
    byte_beat = ByteBeat()
    byte_beat.play()

