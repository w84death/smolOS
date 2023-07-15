from ws2812 import WS2812
import utime
import _thread

class neo_pixel():
    def __init__(self):
        self.thread_running = False
        self.power = machine.Pin(11,machine.Pin.OUT)
        self.power.value(1)
        self.led_pixel = WS2812(12,1)
        print("NeoPixel: Initialized.\bUse pixel.start(), pixel.stop(), pixel.rainbow(), pixel.color(\"r,g,b\").")

    def color(self,rgb_color=""):
        color = tuple(map(int, rgb_color.split(',')))
        self.led_pixel.pixels_fill(color)
        self.led_pixel.pixels_show()
    def rainbow(self):
        self.thread_running = True
        _thread.start_new_thread(self.rainbow_thread,())

    def rainbow_thread(self):
        self.led_pixel.rainbow_cycle(0.001)

    def stop(self):
        self.thread_running = False
        print("NeoPixel: Hearthbeat stopped. Use pixel.start()")

    def start(self):
        if not self.thread_running:
            self.thread_running = True
            _thread.start_new_thread(self.hearthbeat,())
            print("NeoPixel: Hearthbeat started in background. Use pixel.stop()")
        else:
            print("NeoPixel: Thread already used. Use pixel.stop()")

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

pixel = neo_pixel()

