import machine
import utime
import neopixel
import math
from font import Font

BLANK_COLOR = (0,0,0)
BACKGROUND_COLOR = (0,0,0)
FORGROUND_COLOR = (64,12,12)
DELEAY=0.08
PAUSE=0.12
SCREEN_LEN=5*5
        
class Scroller():
    def __init__(self):
        self.pixels = neopixel.NeoPixel(machine.Pin(29),SCREEN_LEN)
        self.pixels.fill((0,0,0))
        self.pixels.write()
        self.font = Font()

    def draw(self,bitmap,offset=0):
        pixel_color = BACKGROUND_COLOR
        for i in range(25):
            if i+offset<0 or i+offset>len(bitmap)-1:
                pixel_color=BACKGROUND_COLOR
            else:
                if bitmap[i+offset]:
                    pixel_color=FORGROUND_COLOR
                else:
                   pixel_color=BACKGROUND_COLOR
            self.pixels[24-i]=pixel_color
        self.pixels.write()

    def draw_text(self, text=""):
        if text=="":
            return
        print(f"Scrolling text: {text}")
        print("Press Ctrl+C to quit.\n")
        while True:
            try:
                for glyf in text:
                    self.marquee(self.font.get_glyf_bitmap(glyf.lower()))
            except KeyboardInterrupt:
                self.pixels.fill(BLANK_COLOR)
                self.pixels.write()
                break
                
    def marquee(self,bitmap,loop=False):
        offset=-SCREEN_LEN
        bit_len=len(bitmap)
        while True:
            self.draw(bitmap,offset)
            if offset==0 and bit_len == SCREEN_LEN:
                utime.sleep(PAUSE)
            else:
                utime.sleep(DELEAY)
            offset += 5
            if offset >= bit_len:
                offset=-SCREEN_LEN
                if not loop:
                    return

    def run(self, message="Specialized Microcontroller-Oriented Lightweight Operating System"):
        self.draw_text(message)

if __name__ == '__main__':
    scroller = Scroller()
    scroller.run()
