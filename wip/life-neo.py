"""
Game of Life implementation for  NeoPixel Grid 5x5 BFF

(c)2023/07 Krzysztof Krystian Jankowski
Homepage: https://smol.p1x.in/os/
"""

import machine
import neopixel
import _thread
import utime
import random

class LifeNeo:
    """
    A class to handle a Game of Life simulation for a 5x5 NeoPixel grid.
    """
    BREATHE_DELAY = 0.2
    HEARTBEAT_DELAY = 0.05

    def __init__(self):
        """
        Initialize the Life object.
        """
        self.thread_running = False
        self.pixels = neopixel.NeoPixel(machine.Pin(29), 5 * 5)
        self.world = [[0 for _ in range(5)] for _ in range(5)]
        self.temp = [[0 for _ in range(5)] for _ in range(5)]
        self.disp = [[0 for _ in range(5)] for _ in range(5)]
        self.pixels.fill((5, 32, 10))
        self.pixels.write()

    def random_seed(self):
        """
        Set a random initial state for the Game of Life.
        """
        for i in range(5):
            for j in range(5):
                self.world[i][j] = random.randint(0, 1)
                self.disp[i][j] = 0

    def update_world(self):
        """
        Update the state of the Game of Life based on the temporary state.
        """
        for i in range(5):
            for j in range(5):
                self.world[i][j] = self.temp[i][j]

    def get_cell_value(self, i, j):
        """
        Get the value of a cell in the Game of Life.
        """
        if i < 0 or i >= 5 or j < 0 or j >= 5:
            return 0
        return self.world[i][j]

    def check_world(self):
        """
        Check the state of the Game of Life and update the temporary state based on the rules of the Game of Life.
        """
        stable = True
        for i in range(5):
            for j in range(5):
                density = 0
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx != 0 or dy != 0:
                            density += self.get_cell_value(i + dx, j + dy)
                if self.world[i][j] == 1:
                    if density < 2 or density > 3:
                        self.temp[i][j] = 0
                        stable = False
                    else:
                        self.temp[i][j] = 1
                else:
                    if density == 3:
                        self.temp[i][j] = 1
                        stable = False
                    else:
                        self.temp[i][j] = 0
        return not stable

    def draw_world(self, forground=(0, 16, 4)):
        """
        Display the state of the Game of Life on the NeoPixel grid.
        """
        background = (0, 0, 10)
        for i in range(5):
            for j in range(5):
                if self.world[i][j] == 1:
                    self.disp[i][j] = 10
                    color = forground
                else:
                    if self.disp[i][j] > 1:
                        self.disp[i][j] -= 2
                    color = (0, int(self.disp[i][j] * 0.25), self.disp[i][j])
                self.pixels[i * 5 + j] = color
        self.pixels.write()

    def simulate(self):
        """
        Simulate the Game of Life.
        """
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
                self.draw_world((12, 12, 0))
                utime.sleep(0.5)

    def start_threaded(self, fn):
        """
        Start a function in a new thread.
        """
        if not self.thread_running:
            self.thread_running = True
            _thread.start_new_thread(fn, ())
            print("Game of Life: Simulation started in background. Use life.stop()")
        else:
            print("Game of Life: Thread is busy. Stop program in background.")

    def start_unthreaded(self):
        """
        Start the simulation of the Game of Life in a new thread.
        """
        self.start_threaded(self.simulate)

    def stop(self):
        """
        Stop the simulation of the Game of Life.
        """
        self.thread_running = False
        print("Game of Life: Thread stopped. Use life.begin()")

# life = LifeNeo()
# life.start_threaded()  # to start in a new thread
# life.start_unthreaded()  # to run in the current thread
