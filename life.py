# Game of Life implementation for NeoPixel Grid 5x5 BFF
# Port by Krzysztof Krystian Jankowski
# (c)203.07

import utime
import _thread
import time
import neopixel
import math
import random

class Life():
    def __init__(self):
        self.world = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.temp  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.world_size = 25
        self.period = 0
        self.delay = 0.333
        self.thread_running = False       
        self.pixels = np = neopixel.NeoPixel(machine.Pin(29),5*5)
        self.pixels.fill((5,32,10))
        self.pixels.write()

    def random_seed(self):
        for i in range(self.world_size):
            self.world[i] = random.randint(0,1)

    def update_world(self):
        for i in range(self.world_size):
            self.world[i] = self.temp[i]

    def get_cell_value(self,i):
        if i<0 or i>=len(self.world):
            return 0
        return self.world[i]
    
    def check_world(self):
        i=0
        stable = True
        for cell in self.world:
            density=0
            density += self.get_cell_value(i-1)
            density += self.get_cell_value(i+1)
            density += self.get_cell_value(i-6)
            density += self.get_cell_value(i-5)
            density += self.get_cell_value(i-4)
            density += self.get_cell_value(i+4)
            density += self.get_cell_value(i+5)
            density += self.get_cell_value(i+6)
            if cell == 1:
                if density<2 or density>3:
                    self.temp[i] = 0
                    stable=False
                else:
                    self.temp[i] = 1
            if cell == 0:
                if density==3:
                    self.temp[i] = 1
                    stable=False
                else:
                    self.temp[i]=0
            i+=1
        return not stable
    
    def draw_world(self):
        palette = [(0,0,5),(0,32,5)]
        for i in range(self.world_size):
            self.pixels[i]=palette[self.world[i]]
        self.pixels.write()
    
    def simulate(self):
        self.random_seed()
        self.draw_world()
        while self.thread_running:
            if self.check_world():
                self.update_world()
                self.draw_world()
                utime.sleep(self.delay)
            else:
                utime.sleep(1)
                self.random_seed()
                self.draw_world()
                utime.sleep(1)
                    
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