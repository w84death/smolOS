# Game of Life implementation for NeoPixel Grid 5x5 BFF
# Port by Krzysztof Krystian Jankowski
# (c)2023.07

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
        self.disp   = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.world_size = 25
        self.period = 0
        self.delay = 0.2
        self.thread_running = False       
        self.pixels = np = neopixel.NeoPixel(machine.Pin(29),5*5)
        self.pixels.fill((5,32,10))
        self.pixels.write()

    def random_seed(self):
        for i in range(self.world_size):
            self.world[i] = random.randint(0,1)
            self.disp[i] = 0
            
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
    
    def draw_world(self,forground=(0,16,4)):
        background = (0,0,10)
        for cell in range(self.world_size):
            if self.world[cell] == 1:
                self.disp[cell] = 10
                color=forground
            else:
                if self.disp[cell]>1:
                    self.disp[cell] -= 2                
                color = (0,int(self.disp[cell]*0.25),self.disp[cell])
            
            self.pixels[cell]=color
        self.pixels.write()
    
    def simulate(self):
        self.random_seed()
        self.draw_world()
        while self.thread_running:
            if self.check_world():
                self.update_world()
                for _ in range(3):
                    self.draw_world()
                    utime.sleep(self.delay)
            else:
                for _ in range(10):
                    self.draw_world()
                    utime.sleep(self.delay)
                self.random_seed()
                self.draw_world((12,12,0))
                utime.sleep(0.5)
                    
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
