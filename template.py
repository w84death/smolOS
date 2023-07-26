"""
Template for user programs for smolOS

(c)2023/07 Krzysztof Krystian Jankowski
Homepage: https://smol.p1x.in/os/
"""

import time
import _thread

# Define constants
MESSAGE_INTERVAL = 10

class Template:
    """
    A template for user programs for smolOS.
    """
    def __init__(self):
        """
        Initialize the Template object.
        """
        self.name = "Template Program"
        self.thread_running = False
        self.msg("Program initialized")
    
    def loop(self):
        """
        Loop where the main logic of the program goes.
        """
        t = 0
        while self.thread_running:
            if t % MESSAGE_INTERVAL == 0:
                self.msg(f"{t}th!")
            time.sleep(1)
            t += 1
            
    def msg(self, message):
        """
        Print a message from the program.
        """
        print(f"{self.name} : {message}")
        
    def stop(self):
        """
        Stop the program.
        """
        self.thread_running = False
        self.msg("Program stopped. Bye!")
        
    def start_threaded(self):
        """
        Start the program in a new thread.
        """
        if not self.thread_running:
            self.thread_running = True
            _thread.start_new_thread(self.loop, ())
            self.msg("Program loop started in background.")
        else:
            self.msg("Thread is busy. Stop program in background.")
        
    def start_unthreaded(self):
        """
        Run the program in the current thread.
        """
        self.thread_running = True
        self.loop()

# template = Template()
# template.start_threaded()  # to start in a new thread
# template.start_unthreaded()  # to run in the current thread
