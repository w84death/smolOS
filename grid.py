# App for controlling Adafruit NeoPixel BFF 5x5 LED Grid
import utime
import _thread
import time
import neopixel

class neo_grid():
    def __init__(self):
        self.thread_running = False
        
        self.pixels = np = neopixel.NeoPixel(machine.Pin(29),5*5)
        self.pixels.fill(0)
        self.pixels.write()
        self.palette = [(12,0,0),(255,128,32)]
        self.heart_bitmap = [
            0,1,1,0,0,
            1,1,1,1,0,
            0,1,1,1,1,
            1,1,1,1,0,
            0,1,1,0,0,
        ]

        print("NeoPixel Grid: Initialized.\bUse grid.start(), grid.stop(), grid.rainbow(), grid.color(\"r,g,b\"), grid.hearth().")

    def draw(self,bitmap):
        i=0
        for pixel in bitmap:
            self.pixels[i]=self.palette[pixel]
            i=i+1
        self.pixels.write()

    def hearth(self):
        self.draw(self.heart_bitmap)

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
            _thread.start_new_thread(self.hearthbeat,())
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


