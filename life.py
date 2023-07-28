"""
Game of Life implementation for smolOS (serial)

(c)2023/07 Krzysztof Krystian Jankowski
Homepage: https://smol.p1x.in/os/
"""

import utime
import time
import math
import random

# Define constants
WORLD_WIDTH = 15
WORLD_HEIGHT = 5
DELAY = 0.05

class Life:
    """
    A class to handle the Life functionalities.
    """
    def __init__(self):
        """
        Initialize the Life object.
        """
        self.world_width = WORLD_WIDTH
        self.world_height = WORLD_HEIGHT
        self.delay = DELAY
        self.world = []
        self.temp  = []
        self.world_size = self.world_width*self.world_height
        self.period = 0
        self.initialize_world()

    def initialize_world(self):
        """
        Initialize the world with zero cells.
        """
        for _ in range(self.world_size):
            self.world.append(0)
            self.temp.append(0)

    def random_seed(self):
        """
        Randomly seed the world.
        """
        for i in range(self.world_size):
            self.world[i] = random.getrandbits(1)

    def update_world(self):
        """
        Update the world with the temporary world.
        """
        for i in range(self.world_size):
            self.world[i] = self.temp[i]

    def get_cell_value(self,i):
        """
        Get the cell value.
        """
        if i<0 or i>=len(self.world):
            return 0
        return self.world[i]

    def check_world(self):
        """
        Check the world for the next generation.
        """
        i=0
        off=self.world_width
        stable = True

        for cell in self.world:
            # Check eight closest cells
            density=0
            if i%self.world_size-1>0:
                density += self.get_cell_value(i-1)
            if i%self.world_size-1<self.world_width:
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
                else: # In good conditions life is going forward
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
        """
        Draw the world.
        """
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

    def run(self):
        """
        Simulate the Life.
        """
        self.random_seed()
        self.draw_world()
        print("Press Ctrl+C to quit.\n")
        while True:
            try:
                if self.check_world():
                    self.update_world()
                    self.draw_world()
                    utime.sleep(self.delay)
                    self.period+=1
                else:
                    utime.sleep(1)
                    self.random_seed()
                    self.period=0
            except KeyboardInterrupt:
                break

if __name__ == '__main__':
    life = Life()
    life.run()


