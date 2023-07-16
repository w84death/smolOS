# App for controlling Adafruit NeoPixel BFF 5x5 LED Grid
import utime
import _thread
import time
import neopixel
import math

class neo_grid():
    def __init__(self):
        self.thread_running = False
        
        self.pixels = np = neopixel.NeoPixel(machine.Pin(29),5*5)
        self.pixels.fill((0,0,0))
        self.pixels.write()
        self.brightness = 0.2
        self.palette = [
            (0,0,0),
            (100,100,100),
            (100,50,50),
            (100,20,20),
            (50,0,50),
            (0,0,200),
            (10,0,200),
            (0,0,50),
            (0,0,50),
            (200,200,100)]

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
        
        # smolOS
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


        print("NeoPixel Grid: Initialized.\bUse grid.demo(), grid.stop(), grid.color(\"r,g,b\"), grid.hearth().")

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
        #self.start(self.plasma)
        self.start(self.marquee)

    def stop(self):
        self.thread_running = False
        print("NeoPixel: Thread stopped. Use grid.start()")

    def start(self,fn):
        if not self.thread_running:
            self.thread_running = True
            _thread.start_new_thread(fn,())
            print("NeoPixel: Demo thread started in background. Use grid.stop()")
        else:
            print("NeoPixel: Thread already used. Use grid.stop()")

grid = neo_grid()
grid.demo()
