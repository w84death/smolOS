# Game of Life implementation for smolOS (serial)
# Port by Krzysztof Krystian Jankowski
# (c)2023.07

import utime
import time
import math
import random

class Life():
    def __init__(self):
        self.world_width = 10
        self.world_height = 5
        self.delay = 0.05
        self.world = []
        self.temp  = []
        self.world_size = self.world_width*self.world_height
        self.period = 0
        for _ in range(self.world_size):
            self.world.append(0)
            self.temp.append(0)

    def random_seed(self):
        for i in range(self.world_size):
            self.world[i] = random.getrandbits(1)
            
    def update_world(self):
        for i in range(self.world_size):
            self.world[i] = self.temp[i]

    def get_cell_value(self,i):
        if i<0 or i>=len(self.world):
            return 0
        return self.world[i]
    
    def check_world(self):
        i=0
        off=self.world_width
        stable = True
        
        for cell in self.world:
            # Check eight closest cells
            density=0
            density += self.get_cell_value(i-1)
            density += self.get_cell_value(i+1)
            density += self.get_cell_value(i-off+1)
            density += self.get_cell_value(i-off)
            density += self.get_cell_value(i-off-1)
            density += self.get_cell_value(i+off+1)
            density += self.get_cell_value(i+off)
            density += self.get_cell_value(i+off-1)
            
            # The rules of life..
            if cell == 1: # Cell is alive
                if density<2 or density>3: # In overcrouded or to lonely conditions life is no more
                    self.temp[i] = 0
                    stable=False
                else: # In bood conditions life is going forward
                    self.temp[i] = 1
            if cell == 0: # Cell is empty
                if density==3: # In good conditions new life is born
                    self.temp[i] = 1
                    stable=False
                else: # Still empty
                    self.temp[i]=0 
            i+=1
        return not stable
    
    def draw_world(self):
        print("\033[2J")
        line = ""
        for cell in range(len(self.world)):
            if self.world[cell] == 1:
                line += "█"
            else:
                line += "░"
            if (cell+1)%self.world_width==0:
                print(line)
                line=""
        print("Period:",self.period)
    
    def simulate(self):
        self.random_seed()
        self.draw_world()
        while True:
            if self.check_world():
                self.update_world()
                self.draw_world()
                utime.sleep(self.delay)
                self.period+=1
            else:
                if input("Continue? [yes]/no >")=="no":
                    return
                else:
                    utime.sleep(1)
                    self.random_seed()
                    self.period=0
                    
    def begin(self):
        self.simulate()

life = Life()
life.begin()
