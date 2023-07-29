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
WORLD_WIDTH = 25
WORLD_HEIGHT = 8
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
        self.world = []
        self.future_world  = []
        self.world_size = self.world_width*self.world_height
        self.period = 0
        self.initialize_world()

    def initialize_world(self):
        """
        Initialize the world with zero cells.
        """
        for _ in range(self.world_size):
            self.world.append(0)
            self.future_world.append(0)

    def random_seed(self):
        """
        Randomly seed the world.
        """
        for i in range(self.world_size):
            self.world[i] = random.getrandbits(1)

    def update_world(self):
        """
        Update the world with calculated next state of the world
        """
        for i in range(self.world_size):
            self.world[i] = self.future_world[i]

    def get_cell_value(self,i):
        """
        Returns 0 if asking for a cell outside the world.
        """
        if i<0 or i>=len(self.world):
            return 0
        return self.world[i]

    def check_world(self):
        """
        Check the world for the next generation.
        """
        i=0
        offset=WORLD_WIDTH
        stable = True

        for cell in self.world:
            # Check eight closest cells
            density=0

            # left and right
            # cell is not on the left edge
            if i%WORLD_WIDTH-1>0:
                density += self.get_cell_value(i-1)
            # cell is not on the right edge
            if i%WORLD_WIDTH-1<WORLD_WIDTH:
                density += self.get_cell_value(i+1)

             # top row
            density += self.get_cell_value(i-offset+1)
            density += self.get_cell_value(i-offset)
            density += self.get_cell_value(i-offset-1)

            # bottom row
            density += self.get_cell_value(i+offset+1)
            density += self.get_cell_value(i+offset)
            density += self.get_cell_value(i+offset-1)

            # The rules of life..
            # Cell is alive
            if cell == 1:

                # In overcrouded or to lonely = life is no more
                if density<2 or density>3:
                    self.future_world[i] = 0
                    stable=False

                # In good conditions life is going forward
                else:
                    self.future_world[i] = 1

            # Cell is empty
            if cell == 0:

                # In good conditions new life is born
                if density==3:
                    self.future_world[i] = 1
                    stable=False

                # Still empty
                else:
                    self.future_world[i]=0

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

    def simulate(self, delay):
        self.random_seed()
        self.draw_world()
        print("Press Ctrl+C to quit.\n")
        while True:
            try:
                if self.check_world():
                    self.update_world()
                    self.draw_world()
                    utime.sleep(delay)
                    self.period+=1
                else:
                    utime.sleep(1)
                    self.random_seed()
                    self.period=0
            except KeyboardInterrupt:
                break

    def run(self, delay=DELAY):
        self.simulate(delay)

if __name__ == '__main__':
    life = Life()
    life.run()


