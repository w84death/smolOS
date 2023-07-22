# Template for user programs for smolOS
#

import time
import _thread

class Template():
    def __init__(self):
        self.name = "Template Program"
        self.thread_running = False
        
        self.msg("Program initialized")
    
    def loop(self):
        # your code goes here..
        # sample loop
        t = 0
        while self.thread_running:
            if t%10==0:
                self.msg(str(t)+"th!")
            time.sleep(1)
            t += 1
            
    def msg(self,msg):
        print(self.name,":",msg)
        
    def stop(self):
        self.thread_running = False
        self.msg("Program stopped. Bye!")

    def start(self, threaded=True):
        if threaded:
            if not self.thread_running:
                self.thread_running = True
                _thread.start_new_thread(self.loop,())
                self.msg("Program loop started in background.")
            else:
                self.msg("Thread is busy. Stop program in background.")
        else:
            self.thread_running = True
            self.loop()
            
template = Template()