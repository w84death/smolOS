import utime
import _thread
import time
import neopixel
import math
import random

class Life():
    def __init__(self):
        self.world_live = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.world_next = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.world_size = 25
        self.period = 0
        self.delay = 0.1
        self.thread_running = False       
        self.pixels = np = neopixel.NeoPixel(machine.Pin(29),5*5)
        self.pixels.fill((5,32,10))
        self.pixels.write()

    def random_seed(self):
        for i in range(self.world_size):
            self.world_live[i] = random.randint(0,1)

    def update_world(self):
        self.world_live = self.world_next
        
    def check_cell(self,cells):
        alive = True
        density = 0
        for cell in cells:
            density+=cell
        if cells[4]==0 and density==4:
            alive = True
        if cells[4]==1 and (density<=3 or density>4):
            alaive = False
        return alive
    
    def draw_world(self):
        palette = [(0,0,0),(12,64,12)]
        for i in range(self.world_size):
            self.pixels[i]=palette[self.world_live[i]]
        self.pixels.write()
    
    def simulate(self):
        self.random_seed()
        self.draw_world()
        while self.thread_running:
            self.random_seed()
            self.draw_world()
            utime.sleep(0.333)
        
    def begin(self):
        self.start(self.simulate)

    def stop(self):
        self.thread_running = False
        print("Game of Life: Thread stopped. Use life.begin()")

    def start(self,fn):
        if not self.thread_running:
            self.thread_running = True
            _thread.start_new_thread(fn,())
            print("Game of Life: Simulation started in background. Use life.stop()")
        else:
            print("Game of Life: Thread is busy. Stop program in background.")

life = Life()
life.begin()