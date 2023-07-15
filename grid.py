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
            (0,0,20),
            (25,7,21),
            (234,0,25),
            (19,0,20)]
        
        self.hearth_bitmap = [
            0,4,4,0,0,
            3,3,3,4,0,
            0,2,3,3,4,
            2,2,3,3,0,
            0,2,2,0,0,
        ]

        self.empty_bitmap = [
            0,0,0,0,0,
            0,0,0,0,0,
            0,0,0,0,0,
            0,0,0,0,0,
            0,0,0,0,0,
        ]
        self.p1x_bitmap = [
            0,0,0,0,0,
            0,0,0,0,0,
            0,0,0,0,0,
            0,0,0,0,0,
            0,0,0,0,0,
            1,1,1,1,1,
            1,0,1,0,0,
            1,1,1,0,0,
            0,0,0,0,0,
            1,1,1,1,1,
            0,0,0,0,0,
            1,1,0,1,1,
            0,0,1,0,0,
            1,1,0,1,1,
            0,0,0,0,0,
            0,0,0,0,0,
            0,0,0,0,0,
            0,0,0,0,0,
            0,0,0,0,0,
            0,0,0,0,0,            
            0,0,0,0,0,
        ]


        print("NeoPixel Grid: Initialized.\bUse grid.start(), grid.stop(), grid.rainbow(), grid.color(\"r,g,b\"), grid.hearth().")

    def draw(self,bitmap,offset=0):
        i=0
        for i in range(25):
            if i<25:
                self.pixels[24-i]=self.palette[bitmap[i+offset]]
            i=i+1
            
        self.pixels.write()

    def test(self):
        while self.thread_running:
            self.pixels.fill(self.palette[0])
            self.pixels.write()
            utime.sleep(1)
            
            self.draw(self.hearth_bitmap)
            utime.sleep(2)
            
            self.draw(self.p1x_bitmap)
            utime.sleep(2)
            
            self.pixels.fill((255,0,0))
            self.pixels.write()
            utime.sleep(0.1)
            self.pixels.fill((0,255,0))
            self.pixels.write()
            utime.sleep(0.1)
            self.pixels.fill((0,0,255))
            self.pixels.write()
            utime.sleep(0.1)
             
    def marquee(self):
        offset=0
        speed=0.1
        while self.thread_running:
            self.draw(self.p1x_bitmap,offset)
            utime.sleep(speed)
            offset += 5
            if offset > 14*5:
                offset=0
    
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
        print("NeoPixel: Hearthbeat stopped. Use np.start()")

    def start(self):
        if not self.thread_running:
            self.thread_running = True
            _thread.start_new_thread(self.marquee,())
            print("NeoPixel: Hearthbeat started in background. Use np.stop()")
        else:
            print("NeoPixel: Thread already used. Use np.stop()")

    def hearthbeat(self):
        heartbeat_pattern = [0, 10, 20, 50, 100, 255, 200, 100, 50, 30, 20, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # pattern for heartbeat
        while self.thread_running:
            for brightness in heartbeat_pattern:
                red = int((255 * brightness) / 255)
                green = int((105 * brightness) / 255)
                blue = int((180 * brightness) / 255)

                self.led_pixel.pixels_fill((red, green, blue))
                self.led_pixel.pixels_show()
                utime.sleep(0.05)

grid = neo_grid()
grid.start()

