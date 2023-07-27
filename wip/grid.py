# This code will be moved to scroller
# Lot of refactoring here
# App for controlling Adafruit NeoPixel BFF 5x5 LED Grid
import utime
import _thread
import time
import neopixel
import math
import random

class neo_grid():
    def __init__(self):
        self.thread_running = False
        self.scroll_running = True
        
        self.pixels = np = neopixel.NeoPixel(machine.Pin(29),5*5)
        self.pixels.fill((0,0,0))
        self.pixels.write()
        self.brightness = 0.2
        self.palette = [
            (0,0,0),
            (50,50,50),
            (50,25,25),
            (50,10,10),
            (25,0,25),
            (10,10,10),
            (124,54,23),
            (3,12,10),
            (0,0,25),
            (100,100,50)]

        self.hearth_bitmap = [
            4,1,1,4,4,
            1,1,1,1,4,
            4,1,1,1,1,
            1,1,1,1,4,
            4,1,1,4,4,
        ]

        self.hearth_color_bitmap = [
            0,2,2,0,0,
            2,1,3,3,0,
            0,2,3,3,4,
            3,3,3,4,0,
            0,4,4,0,0,
        ]
        self.p1x_bitmap = [
            0,0,0,0,0,
            5,5,5,5,5,
            0,5,5,5,0,
            0,0,5,0,0,
            0,0,0,0,0,
            1,1,1,1,1,
            1,0,1,0,0,
            1,1,1,0,0,
            0,5,0,0,0,
            1,1,1,1,1,
            0,0,0,0,0,
            1,1,0,1,1,
            0,0,1,0,0,
            1,1,0,1,1,
            0,0,0,0,0,
            0,0,5,0,0,
            0,5,5,5,0,
            5,5,5,5,5,            
            0,0,0,0,0,
            
        ]

        # smolOS banner
        self.logo_bitmap=[
            8,8,8,8,9,
            8,8,9,8,9,
            8,9,8,9,8,
            8,9,8,8,8,
            8,8,8,8,8,
            8,8,8,9,9,
            8,8,9,9,8,
            8,8,9,9,9,
            8,8,9,9,8,
            8,8,8,8,8,
            8,8,8,9,9,
            8,8,9,8,9,
            8,8,9,9,8,
            8,8,8,8,8,
            8,8,8,9,9,
            8,9,9,8,8,
            8,8,8,8,8,
            8,8,9,9,8,
            8,9,8,8,9,
            9,8,8,8,9,
            9,8,8,9,8,
            8,9,9,8,8,
            8,8,8,8,9,
            8,9,9,8,9,
            9,8,8,9,8,
            9,8,8,8,8,
            8,8,8,8,8,
        ]

        print("NeoPixel Grid: Initialized.\bUse grid.demo(), grid.stop(), grid.color(\"r,g,b\").")

    def draw(self,bitmap,offset=0,bg=(0,0,0)):
        bit_len=len(bitmap)
        padding=100
        bright=0.0
        for i in range(25):
            if i+offset<0 or i+offset>bit_len-1:
                #gradient
                if i%5==0:
                    if offset<0:
                        bright = (padding+offset)*0.005
                    else:
                        bright = (padding-(offset-bit_len))*0.005
                r=int(bg[0]*bright)
                g=int(bg[1]*bright)
                b=int(bg[2]*bright)
                
                self.pixels[24-i]=(r,g,b)
            else:
                self.pixels[24-i]=self.palette[bitmap[i+offset]]
        self.pixels.write()

    def draw_text(self, text=""):
        if text=="":
            return
        while self.thread_running:
            for glyf in text:
                if not self.thread_running: return
                self.draw(self.get_glyf_bitmap(glyf.lower()))
                utime.sleep(0.33)

    def marquee(self,bitmap,bg=0,loop=False):
        screen_len=25
        offset_len=100
        offset=-offset_len
        delay=0.08
        pause=0.12
        bit_len=len(bitmap)
        while self.scroll_running:
            self.draw(bitmap,offset,self.palette[bg])
            if offset==0 and bit_len == screen_len:
                utime.sleep(pause)
            else:
                utime.sleep(delay)
            offset += 5
            if offset >= bit_len+offset_len:
                offset=-offset_len
                if not loop:
                    return
            if not self.scroll_running:
                return                

    def draw_random_numbers(self):
        while self.thread_running:
            self.draw(self.get_glyf_bitmap(str(random.randint(0,9))))
            utime.sleep(0.25)
    
    def draw_all_glyfs(self):
        while self.thread_running:
            for glyf in ("01234567890abcdefghijklmnopqrstuvwxyz"):
                if not self.thread_running: return
                self.draw(self.get_glyf_bitmap(glyf))
                utime.sleep(0.25)

    def draw_sample_message(self):
        while self.thread_running:
            self.draw_text(" - Hello, Welcome to the smollO..with neopixel grid! - ")
        
    def get_glyf_bitmap(self,glyf):
        glyfs = {"h":"0x1ff93e0","k":"0x1f3ea60","j":"0x30ffc0","n":"0x1f61be0","o":"0xefc5c0","t":"0x10ffe00","u":"0x1ef87e0","q":"0xdf45c0","p":"0xffd180","s":"0x1ded6e0"," ":"0x0","r":"0xffd9a0","v":"0x1ef9b80","w":"0x1f1907f",",":"0x110000","y":"0x18f9f00","x":"0x1bf93e0",".":"0x318000","z":"0x13bf720","!":"0xef7a0","-":"0x421080","5":"0x1dedee0","4":"0x1e13c40","7":"0x119db80","6":"0x1ffd6e0","1":"0x8ffc00","0":"0xeccdc0","3":"0x11afdc0","2":"0x199dfa0","d":"0x1ffc5c0","e":"0x1ffd620","f":"0x1ffd200","a":"0xfde9e0","9":"0x1ca5de0","8":"0x1fad5e0","b":"0x1ffd540","c":"0xefc540","g":"0xe8dcc0","l":"0xff8440","m":"0x1fe3b9f","i":"0xffc00"}
        return self.hex_to_bitmap(glyfs[glyf])
    
    def hex_to_bitmap(self,hex_string):
        binary_string = bin(int(hex_string, 16))[2:]
        binary_string =  '0' * (25 - len(binary_string)) + binary_string
        binary_array = [int(bit) for bit in binary_string]
        return binary_array
        
    def bitmap_to_hex(self,bitmap):
        binary_string = ''.join(str(bit) for bit in bitmap )
        hex_value = hex(int(binary_string, 2))
        print(hex_value)

    def hearth(self):
        self.draw(self.hearth_bitmap)

    def color(self,rgb_color=(0,0,0)):
        self.pixels.fill(rgb_color)
        self.pixels.write()

    def scroller(self):
        while self.thread_running:
            self.marquee(self.p1x_bitmap,5)
            self.marquee(self.hearth_bitmap,4)
            self.marquee(self.logo_bitmap,8)
            self.marquee(self.logo_bitmap,8,True)
            
        self.color()
        
    def demo(self):
        self.start(self.scroller)

    def stop(self):
        self.thread_running = False
        self.scroll_running = False
        utime.sleep(0.5)
        self.scroll_running = True
        print("NeoPixel: Thread stopped. Use grid.start()")

    def start(self,fn):
        if not self.thread_running:
            self.thread_running = True
            _thread.start_new_thread(fn,())
            print("NeoPixel: Demo thread started in background. Use grid.stop()")
        else:
            print("NeoPixel: Thread already used. Use grid.stop()")

#grid = neo_grid()
#grid.demo()

