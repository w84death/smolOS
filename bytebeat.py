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

sin = math.sin
BUZZER_PIN = 4
BUZZER_DUTY = 8000
PI  =  3.1415926535
PI2 = PI*2
NEOPIXEL_PIN = 12
NEOPIXELS_PIN = 29

class ByteBeat:

    def __init__(self):
        self.t = 0
        machine.freq(260000000) # 260MHz
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
        return [
            int((127+128*sin((t>>8)+10.9714)*PI2)*.1),
            int((127+128*sin((1.14286*(t>>13)+10.9714+(0.05*sin(t>>13)))*PI2+1+8*sin(t>>8)*0.01))),
            int((15+16*sin((4.8*(t>>12)+3.36))/32))]

    def start(self):
        while True:
            try:
                bb=self.bytebeat(self.t)
                bites = 32 + (bb[0] & bb[1] | bb[2])*2
                self.buzzer.freq(bites)
                self.t += 1

                color = (int(bb[0]%255),int(bb[1]%255),int(bb[2]%255))
                self.pixels.fill(color)
                self.pixel.fill(color)
                self.pixels.write()
                self.pixel.write()

            except KeyboardInterrupt:
                self.buzzer.duty_u16(0)
                break


if __name__ == "__main__":
    byte_beat = ByteBeat()
    byte_beat.start()

