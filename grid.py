# App for controlling Adafruit NeoPixel BFF 5x5 LED Grid
import utime
import _thread
import time
import neopixel

class neo_grid():
    def __init__(self):
        self.thread_running = False
        
        self.pixels = np = neopixel.NeoPixel(machine.Pin(29),5*5)
        self.pixels.fill((0,0,0))
        self.pixels.write()
        self.brightness = 0.2
        self.palette = [
            (0,0,0),
            (10,10,10),
            (10,5,5),
            (10,2,2),
            (5,0,5),
            (0,0,20),
            (1,0,20),
            (0,0,5),
            (0,0,5),
            (20,20,10)]

        self.empty_bitmap = [
            0,0,0,0,0,
            0,0,0,0,0,
            0,0,0,0,0,
            0,0,0,0,0,
            0,0,0,0,0,
        ]
        
        self.hearth_bitmap = [
            0,2,2,0,0,
            2,1,3,3,0,
            0,2,3,3,4,
            3,3,3,4,0,
            0,4,4,0,0,
        ]

        self.p1x_bitmap = [
            6,6,5,5,6,
            6,0,5,0,0,
            5,5,5,0,0,
            0,7,0,0,0,
            6,6,6,6,5,
            0,0,0,0,0,
            6,5,0,6,5,
            0,0,7,0,0,
            6,5,0,6,5,
        ]
        
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


        print("NeoPixel Grid: Initialized.\bUse grid.start(), grid.stop(), grid.rainbow(), grid.color(\"r,g,b\"), grid.hearth().")

    def draw(self,bitmap,offset=0,len=25,bg=(0,0,0)):
        for i in range(25):
            if i<25:
                if i+offset<0 or i+offset>len-1:
                    self.pixels[24-i]=bg
                else:
                    self.pixels[24-i]=self.palette[bitmap[i+offset]]
            i=i+1 
        self.pixels.write()

    def marquee(self):
        screen_len=25
        offset=-50
        fast=0.05
        slow=0.12
        len=(25*5)+1
        bitmap=self.logo_bitmap
        bitmap_id=0
        bg=8
        while self.thread_running:
            self.draw(bitmap,offset,len,self.palette[bg])
            if offset==0 or (len>screen_len and offset<len-10 and offset>0):
                utime.sleep(slow)
                if len==screen_len:
                    utime.sleep(slow*10)
            else:   
                utime.sleep(fast)
            offset += 5
            if offset >= len:
                offset=-50
                bitmap_id+=1
                if bitmap_id>3: bitmap_id=0
                if bitmap_id==0:
                    bitmap=self.logo_bitmap
                    len=(25*5)+5
                    bg=8
                if bitmap_id==2:
                    bitmap=self.p1x_bitmap
                    bg=0
                    len=9*5                
                if bitmap_id in (1,3):
                    bitmap=self.hearth_bitmap
                    len=25
                    bg=4

    def hearth(self):
        self.draw(self.hearth_bitmap)

    def color(self,rgb_color=""):
        return
    
    def rainbow(self):
        return
    
    def rainbow_thread(self):
        return

    def stop(self):
        self.thread_running = False
        print("NeoPixel: Thread stopped. Use grid.start()")

    def start(self):
        if not self.thread_running:
            self.thread_running = True
            _thread.start_new_thread(self.marquee,())
            print("NeoPixel: Marquee thread started in background. Use grid.stop()")
        else:
            print("NeoPixel: Thread already used. Use grid.stop()")

grid = neo_grid()
grid.start()

