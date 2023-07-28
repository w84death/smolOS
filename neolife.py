"""
Game of Life implementation for  NeoPixel Grid 5x5 BFF

(c)2023/07 Krzysztof Krystian Jankowski
Homepage: https://smol.p1x.in/os/
"""

import machine
import neopixel
import utime
import random

# Define constants
WORLD_WIDTH = 5
WORLD_HEIGHT = 5
DELAY = 0.1
BLANK_COLOR = (0,0,0)
BACKGROUND_COLOR = (0, 0, 10)
FORGROUND_COLOR = (64, 24, 18)
NEW_COLOR = (12,8,8)

class Neolife:
    def __init__(self):
        self.world = []
        self.future_world  = []
        self.world_size = WORLD_WIDTH*WORLD_HEIGHT
        self.period = 0
        self.pixels = neopixel.NeoPixel(machine.Pin(29), self.world_size)
        self.pixels.fill(BACKGROUND_COLOR)
        self.pixels.write()

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
            if i%self.world_size-1>0:
                density += self.get_cell_value(i-1)
            # cell is not on the right edge
            if i%self.world_size-1<WORLD_WIDTH:
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

    def draw_world(self, color=FORGROUND_COLOR):
        """
        Display the state of the Game of Life on the NeoPixel grid.
        """
        pixel_color = color
        for cell in range(self.world_size):
            if  self.world[cell] == 0:
                pixel_color = BACKGROUND_COLOR
            elif self.world[cell] == 1:
                pixel_color = color
            self.pixels[cell] = pixel_color
        self.pixels.write()

    def simulate(self, delay):
        self.random_seed()
        self.draw_world()
        print("Press Ctrl+C to quit.\n")
        while True:
            try:
                if self.check_world():
                    self.update_world()
                    for _ in range(3):
                        self.draw_world()
                        utime.sleep(delay)
                else:
                    for _ in range(10):
                        self.draw_world()
                        utime.sleep(delay)
                    self.random_seed()
                    self.draw_world(NEW_COLOR)
                    utime.sleep(0.5)
            except KeyboardInterrupt:
                self.pixels.fill(BLANK_COLOR)
                self.pixels.write()
                break

    def run(self, delay=DELAY):
        self.simulate(delay)

if __name__ == '__main__':
    neolife = Neolife()
    neolife.run()


